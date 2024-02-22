from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Expression, ForeignKey, ManyToOneRel, Model, QuerySet
from django.db.models.constants import LOOKUP_SEP
from graphene.relay.connection import ConnectionOptions
from graphene.utils.str_converters import to_snake_case
from graphene_django.types import DjangoObjectTypeOptions
from graphene_django.utils import maybe_queryset
from graphql import (
    FieldNode,
    FragmentSpreadNode,
    GraphQLField,
    GraphQLOutputType,
    InlineFragmentNode,
    SelectionNode,
)

from .cache import get_from_query_cache, store_in_query_cache
from .errors import OptimizerError
from .settings import optimizer_settings
from .store import QueryOptimizerStore
from .utils import (
    get_field_type,
    get_selections,
    get_underlying_type,
    is_foreign_key_id,
    is_optimized,
    is_to_many,
    is_to_one,
    maybe_skip_optimization_on_error,
)

if TYPE_CHECKING:
    from graphene.types.definitions import GrapheneObjectType, GrapheneUnionType

    from .typing import (
        PK,
        Any,
        Callable,
        GQLInfo,
        Iterable,
        ModelField,
        Optional,
        ToManyField,
        ToOneField,
        TypeOptions,
        TypeVar,
        Union,
    )

    TModel = TypeVar("TModel", bound=Model)
    TCallable = TypeVar("TCallable", bound=Callable)


__all__ = [
    "optimize",
    "QueryOptimizer",
    "required_fields",
    "required_annotations",
]


@maybe_skip_optimization_on_error
def optimize(
    queryset: QuerySet[TModel],
    info: GQLInfo,
    *,
    pk: PK = None,
    max_complexity: Optional[int] = None,
) -> QuerySet[TModel]:
    """
    Optimize the given queryset according to the field selections
    received in the GraphQLResolveInfo.

    :param queryset: Base queryset to optimize from.
    :param info: The GraphQLResolveInfo object used in the optimization process.
    :param pk: Primary key for an item in the queryset model. If set, optimizer will check
               the query cache for that primary key before making query.
    :param max_complexity: How many 'select_related' and 'prefetch_related' table joins are allowed.
                           Used to protect from malicious queries.
    :return: The optimized queryset.
    """
    queryset = maybe_queryset(queryset)

    # Check if prior optimization has been done already
    if is_optimized(queryset):
        return queryset

    field_type = get_field_type(info)
    selections = get_selections(info)
    if not selections:  # pragma: no cover
        return queryset

    optimizer = QueryOptimizer(info)
    store = optimizer.optimize_selections(field_type, selections, queryset.model)

    # When resolving reverse one-to-many relations (other model has foreign key to this model),
    # if `known_related_fields` exist, they should be added to the store, since they are used to linked
    # to the original model based on that field.
    if queryset._known_related_objects:  # pragma: no cover
        store.related_fields += [row.attname for row in queryset._known_related_objects]

    max_complexity = max_complexity if max_complexity is not None else optimizer_settings.MAX_COMPLEXITY
    complexity = store.complexity
    if complexity > max_complexity:
        msg = f"Query complexity of {complexity} exceeds the maximum allowed of {max_complexity}"
        raise OptimizerError(msg)

    if pk is not None:
        cached_item = get_from_query_cache(info.operation, info.schema, queryset.model, pk, store)
        if cached_item is not None:
            queryset._result_cache = [cached_item]
            return queryset

    queryset = store.optimize_queryset(queryset, pk=pk)

    if optimizer.cache_results:
        store_in_query_cache(info.operation, queryset, info.schema, store)

    return queryset


class QueryOptimizer:
    """Query optimizer for Django QuerySets."""

    def __init__(self, info: GQLInfo) -> None:
        self.info = info
        self.cache_results = True

    def optimize_selections(
        self,
        field_type: Union[GrapheneObjectType, GrapheneUnionType],
        selections: tuple[SelectionNode, ...],
        model: type[Model],
    ) -> QueryOptimizerStore:
        store = QueryOptimizerStore(model=model, info=self.info)

        for selection in selections:
            if isinstance(selection, FieldNode):
                self.optimize_field_node(field_type, selection, store)

            elif isinstance(selection, FragmentSpreadNode):
                self.optimize_fragment_spread(field_type, selection, model, store)

            elif isinstance(selection, InlineFragmentNode):
                self.optimize_inline_fragment(field_type, selection, model, store)

            else:  # pragma: no cover
                msg = f"Unhandled selection node: '{selection}'"
                raise OptimizerError(msg)

        return store

    def optimize_field_node(
        self,
        field_type: GrapheneObjectType,
        selection: FieldNode,
        store: QueryOptimizerStore,
    ) -> None:
        options: TypeOptions = field_type.graphene_type._meta

        if isinstance(options, ConnectionOptions):
            return self.handle_connection_node(field_type, selection, store)

        if isinstance(options, DjangoObjectTypeOptions):
            return self.handle_regular_node(field_type, selection, store)

        msg = f"Unhandled field options type: {options}"  # pragma: no cover
        raise OptimizerError(msg)  # pragma: no cover

    def handle_regular_node(
        self,
        field_type: GrapheneObjectType,
        selection: FieldNode,
        store: QueryOptimizerStore,
    ) -> None:
        model: type[Model] = field_type.graphene_type._meta.model
        selection_graphql_name = selection.name.value
        selection_graphql_field = field_type.fields.get(selection_graphql_name)
        if selection_graphql_field is None:  # pragma: no cover
            return

        model_field_name = to_snake_case(selection_graphql_name)
        try:
            if model_field_name == "pk":
                model_field: ModelField = model._meta.pk
                model_field_name = model_field.name  # use actual model pk name, e.g. 'id'
            else:
                model_field: ModelField = model._meta.get_field(model_field_name)
        except FieldDoesNotExist:
            self.check_resolver_hints(selection_graphql_field, model, store)
            return

        if not model_field.is_relation or is_foreign_key_id(model_field, model_field_name):
            store.only_fields.append(model_field_name)

        elif is_to_one(model_field):  # noinspection PyTypeChecker
            self.handle_to_one(model_field_name, selection, selection_graphql_field.type, model_field, store)

        elif is_to_many(model_field):  # noinspection PyTypeChecker
            self.handle_to_many(model_field_name, selection, selection_graphql_field.type, model_field, store)

        else:  # pragma: no cover
            msg = f"Unhandled selection: '{selection.name.value}'"
            raise OptimizerError(msg)

    def check_resolver_hints(self, field: GraphQLField, model: type[Model], store: QueryOptimizerStore) -> None:
        anns: Optional[dict[str, Expression]] = getattr(field.resolve, "annotations", None)
        fields: Optional[tuple[str, ...]] = getattr(field.resolve, "fields", None)

        if anns:
            store.annotations.update(anns)
        if fields is None:  # pragma: no cover
            return

        model_fields: list[ModelField] = model._meta.get_fields()
        for field_name in fields:
            hint_store = QueryOptimizerStore(model=model, info=self.info)
            self.find_field_from_model(field_name, model_fields, hint_store)
            store += hint_store

    def find_field_from_model(
        self,
        field_name: str,
        model_fields: Iterable[ModelField],
        store: QueryOptimizerStore,
        prefix: str = "",
    ) -> None:
        for model_field in model_fields:
            model_field_name = model_field.name
            if prefix:
                model_field_name = f"{prefix}{LOOKUP_SEP}{model_field_name}"

            if field_name == model_field_name:
                store.only_fields.append(model_field.name)
                return None

            if not field_name.startswith(model_field_name):
                continue

            related_model: type[Model] = model_field.related_model  # type: ignore[assignment]
            if related_model is None:  # pragma: no cover
                msg = f"No related model, but hint seems like has one: {field_name!r}"
                raise OptimizerError(msg)
            if related_model == "self":  # pragma: no cover
                related_model = model_field.model

            nested_store = QueryOptimizerStore(model=related_model, info=self.info)
            if is_to_many(model_field):
                store.prefetch_stores[model_field.name] = nested_store
            elif is_to_one(model_field):
                store.select_stores[model_field.name] = nested_store
            else:  # pragma: no cover
                msg = f"Field {model_field} is not a related field."
                raise OptimizerError(msg)

            if isinstance(model_field, ManyToOneRel):
                nested_store.related_fields.append(model_field.field.attname)

            related_model_fields: list[ModelField] = related_model._meta.get_fields()

            return self.find_field_from_model(
                field_name=field_name,
                prefix=model_field_name,
                store=nested_store,
                model_fields=related_model_fields,
            )

        msg = f"Field {field_name!r} not found in fields: {model_fields}."  # pragma: no cover
        raise OptimizerError(msg)  # pragma: no cover

    def handle_connection_node(
        self,
        field_type: GrapheneObjectType,
        selection: FieldNode,
        store: QueryOptimizerStore,
    ) -> None:
        if selection.selection_set is None:  # pragma: no cover
            return

        # Connection QuerySets are sliced, so the results
        # should be cached later in the connection field.
        self.cache_results = False

        node: FieldNode = selection.selection_set.selections[0]  # type: ignore[assignment]
        if node.selection_set is None:  # page info
            return

        edges_field = field_type.fields[selection.name.value]
        edge_type = get_underlying_type(edges_field.type)
        node_field = edge_type.fields[node.name.value]
        node_type = get_underlying_type(node_field.type)
        node_model: type[Model] = node_type.graphene_type._meta.model

        nested_store = self.optimize_selections(node_type, node.selection_set.selections, node_model)
        store += nested_store

    def handle_to_one(
        self,
        model_field_name: str,
        selection: FieldNode,
        selection_field_type: GraphQLOutputType,
        model_field: ToOneField,
        store: QueryOptimizerStore,
    ) -> None:
        if selection.selection_set is None:  # pragma: no cover
            return

        related_model: type[Model] = model_field.related_model  # type: ignore[assignment]
        if related_model == "self":  # pragma: no cover
            related_model = model_field.model

        selection_field_type = get_underlying_type(selection_field_type)
        nested_store = self.optimize_selections(
            selection_field_type,
            selection.selection_set.selections,
            related_model,
        )

        if isinstance(model_field, ForeignKey):
            store.related_fields.append(model_field.attname)

        store.select_stores[model_field_name] = nested_store

    def handle_to_many(
        self,
        model_field_name: str,
        selection: FieldNode,
        selection_field_type: GraphQLOutputType,
        model_field: ToManyField,
        store: QueryOptimizerStore,
    ) -> None:
        if selection.selection_set is None:  # pragma: no cover
            return

        related_model: type[Model] = model_field.related_model  # type: ignore[assignment]
        if related_model == "self":  # pragma: no cover
            related_model = model_field.model

        selection_field_type = get_underlying_type(selection_field_type)
        nested_store = self.optimize_selections(
            selection_field_type,
            selection.selection_set.selections,
            related_model,
        )

        if isinstance(model_field, ManyToOneRel):
            nested_store.related_fields.append(model_field.field.attname)

        store.prefetch_stores[model_field_name] = nested_store

    def optimize_fragment_spread(
        self,
        field_type: GrapheneObjectType,
        selection: FragmentSpreadNode,
        model: type[Model],
        store: QueryOptimizerStore,
    ) -> None:
        graphql_name = selection.name.value
        field_node = self.info.fragments[graphql_name]
        selections = field_node.selection_set.selections
        nested_store = self.optimize_selections(field_type, selections, model)
        store += nested_store

    def optimize_inline_fragment(
        self,
        field_type: GrapheneUnionType,
        selection: InlineFragmentNode,
        model: type[Model],
        store: QueryOptimizerStore,
    ) -> None:
        fragment_type_name = selection.type_condition.name.value
        selection_graphql_field: Optional[GrapheneObjectType]
        selection_graphql_field = next((t for t in field_type.types if t.name == fragment_type_name), None)
        if selection_graphql_field is None:  # pragma: no cover
            return

        fragment_model: type[Model] = selection_graphql_field.graphene_type._meta.model
        if fragment_model != model:  # pragma: no cover
            return

        selections = selection.selection_set.selections
        nested_store = self.optimize_selections(selection_graphql_field, selections, fragment_model)
        store += nested_store


def required_fields(*args: str) -> Callable[[TCallable], TCallable]:
    """
    Add hints to a resolver to require given fields
    in relation to its DjangoObjectType model.

    :param args: Fields that the decorated resolver needs.
                 Related entity fields can also be used with
                 the field lookup syntax (e.g., 'related__field')
    """

    def decorator(resolver: TCallable) -> TCallable:
        resolver.fields = args  # type: ignore[attr-defined]
        return resolver

    return decorator


def required_annotations(**kwargs: Any) -> Callable[[TCallable], TCallable]:
    """
    Add hints to a resolver function indicating that the given annotations
    should be applied to the ObjectType queryset _after_ filters are applied.
    See. https://docs.djangoproject.com/en/dev/topics/db/aggregation/#order-of-annotate-and-filter-clauses

    :param kwargs: Annotations that the decorated resolver needs.
                   Values should be Expression or F-object instances,
                   or any other value that works with queryset.annotate().
    """

    def decorator(resolver: TCallable) -> TCallable:
        resolver.annotations = kwargs  # type: ignore[attr-defined]
        return resolver

    return decorator
