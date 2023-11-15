import strawberry
import datetime
from typing import Optional, Union, List, Annotated
import gql_documents.GraphTypeDefinitions

from .externalIdCategoryGQLModel import ExternalIdCategoryGQLModel


def getLoaders(info):
    return info.context["all"]


UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]


@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing an external type id (like SCOPUS identification / id)""",
)
class ExternalIdTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        if id is None:
            return None
        loader = getLoaders(info=info).externaltypeids
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = (
                cls._type_definition
            )  # some version of strawberry changed :(

        return result

    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Type name""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Type name (en)""")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Initial timestamp""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberry.field(description="""Who created it""")
    def created_by(self) -> Optional["UserGQLModel"]:
        # sync method which returns Awaitable :)
        result = gql_externalids.GraphTypeDefinitions.UserGQLModel.resolve_reference(
            id=self.createdby
        )
        return result

    @strawberry.field(description="""Who updated it""")
    def changed_by(self) -> Optional["UserGQLModel"]:
        # sync method which returns Awaitable :)
        return gql_externalids.GraphTypeDefinitions.UserGQLModel.resolve_reference(
            id=self.changedby
        )

    @strawberry.field(description="""Category which belongs to""")
    def category(
        self, info: strawberry.types.Info
    ) -> Optional["ExternalIdCategoryGQLModel"]:
        # sync method which returns Awaitable :)
        return ExternalIdCategoryGQLModel.resolve_reference(info, id=self.category_id)


#####################################################################
#
# Special fields for query
#
#####################################################################
@strawberry.field(description="""Rows of externaltypeids""")
async def externalidtype_page(
    self,
    info: strawberry.types.Info,
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> List[ExternalIdTypeGQLModel]:
    loader = getLoaders(info).externaltypeids
    rows = await loader.page(skip=skip, limit=limit)
    return rows


@strawberry.field(description="""Rows of externaltypeids""")
async def externalidtype_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> Optional[ExternalIdTypeGQLModel]:
    result = await ExternalIdTypeGQLModel.resolve_reference(info, id)
    return result


#####################################################################
#
# Mutation section
#
#####################################################################
import datetime


@strawberry.input()
class ExternalIdTypeInsertGQLModel:
    name: str = strawberry.field(default=None, description="Name of type")
    name_en: Optional[str] = strawberry.field(
        default=None, description="En name of type"
    )
    urlformat: Optional[str] = strawberry.field(
        default=None, description="Format for conversion of id into url link"
    )
    id: Optional[strawberry.ID] = strawberry.field(
        default=None, description="Could be uuid primary key"
    )
    category_id: Optional[strawberry.ID] = strawberry.field(
        default=None, description="Category of type"
    )
    createdby: strawberry.Private[strawberry.ID]


@strawberry.input()
class ExternalIdTypeUpdateGQLModel:
    id: strawberry.ID = strawberry.field(default=None, description="Primary key")
    lastchange: datetime.datetime = strawberry.field(
        default=None, description="Timestamp"
    )
    name: Optional[str] = strawberry.field(default=None, description="Name of type")
    name_en: Optional[str] = strawberry.field(
        default=None, description="En name of type"
    )
    urlformat: Optional[str] = strawberry.field(
        default=None, description="Format for conversion of id into url link"
    )
    category_id: Optional[strawberry.ID] = strawberry.field(
        default=None, description="Category of type"
    )
    changedby: strawberry.Private[strawberry.ID]


@strawberry.type()
class ExternalIdTypeResultGQLModel:
    id: Optional[strawberry.ID] = strawberry.field(
        default=None, description="Primary key of table row"
    )
    msg: str = strawberry.field(
        default=None, description="""result of operation, should be "ok" or "fail" """
    )

    @strawberry.field(description="""Result of insert operation""")
    async def externaltypeid(
        self, info: strawberry.types.Info
    ) -> Union[ExternalIdTypeGQLModel, None]:
        result = await ExternalIdTypeGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.mutation(description="defines a new external type id for an entity")
async def externaltypeid_insert(
    self, info: strawberry.types.Info, externaltypeid: ExternalIdTypeInsertGQLModel
) -> ExternalIdTypeResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).externaltypeids
    externaltypeid.createdby = actingUser["id"]

    result = ExternalIdTypeResultGQLModel()
    row = await loader.insert(externaltypeid)
    result.id = row.id
    result.msg = "ok"

    return result


@strawberry.mutation(description="Update existing external type id for an entity")
async def externaltypeid_update(
    self, info: strawberry.types.Info, externaltypeid: ExternalIdTypeUpdateGQLModel
) -> ExternalIdTypeResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).externaltypeids
    externaltypeid.changedby = actingUser["id"]

    result = ExternalIdTypeResultGQLModel()
    row = await loader.update(externaltypeid)
    if row is None:
        result.id = None
        result.msg = "fail"
    else:
        result.id = row.id
        result.msg = "ok"

    return result
