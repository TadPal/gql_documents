import strawberry
import datetime
from typing import Union, Optional, List, Annotated
import gql_documents.GraphTypeDefinitions


def getLoaders(info):
    return info.context["all"]


def getUser(info):
    return info.context["user"]


UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]

###########################################################################################################################
#
# zde definujte sve nove GQL modely, kde mate zodpovednost
#
# - venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
#
###########################################################################################################################


@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a document""",
)
class DocumentGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        result = None
        if id is not None:
            loader = getLoaders(info=info).documents
            print(loader, flush=True)
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

    @strawberry.field(description="""Brief description""")
    def description(self) -> str:
        return self.description

    @strawberry.field(description="""Document Name""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Initial timestamp""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberry.field(description="""Author of the document""")
    def author(self) -> Optional["UserGQLModel"]:
        # sync method which returns Awaitable :)
        return gql_documents.GraphTypeDefinitions.UserGQLModel.resolve_reference(
            id=self.author
        )

    @strawberry.field(description="""DSpace id""")
    def dspace_id(self) -> strawberry.ID:
        return self.dspace_id


#####################################################################
#
# Special fields for query
#
#####################################################################
@strawberry.field(description="""Rows of documents""")
async def documents_page(
    self,
    info: strawberry.types.Info,
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> List[DocumentGQLModel]:
    loader = getLoaders(info).documents
    rows = await loader.page(skip=skip, limit=limit)
    return rows


@strawberry.field(description="""Returns document by id""")
async def document_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> Optional[DocumentGQLModel]:
    result = await DocumentGQLModel.resolve_reference(info, id)
    return result


#####################################################################
#
# Mutation section
#
#####################################################################


@strawberry.input()
class DocumentInsertGQLModel:
    dspace_id: strawberry.ID = strawberry.field(
        default=None, description="Primary key of dspace entity"
    )
    description: str = strawberry.field(
        default=None, description="Brief description of document"
    )
    author: strawberry.Private[strawberry.ID] = None


@strawberry.input()
class DocumentUpdateGQLModel:
    dspace_id: strawberry.ID = strawberry.field(
        default=None, description="Primary key of dspace entity"
    )
    description: str = strawberry.field(
        default=None, description="Brief description of document"
    )
    author: strawberry.Private[strawberry.ID] = None


@strawberry.type()
class DocumentResultGQLModel:
    id: Optional[strawberry.ID] = strawberry.field(
        default=None, description="Primary key of table row"
    )
    msg: str = strawberry.field(
        default=None, description="""result of operation, should be "ok" or "fail" """
    )

    @strawberry.field(description="""Result of drone operation""")
    async def document(
        self, info: strawberry.types.Info
    ) -> Union[DocumentGQLModel, None]:
        result = await DocumentGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.mutation(description="defines a new document")
async def document_insert(
    self, info: strawberry.types.Info, document: DocumentInsertGQLModel
) -> DocumentResultGQLModel:
    loader = getLoaders(info).documents

    result = DocumentResultGQLModel()
    rows = await loader.filter_by(dspace_id=document.dspace_id)
    row = next(rows, None)

    if row is None:
        row = await loader.insert(document)
        result.id = row.id
        result.msg = "ok"
    else:
        result.id = row.id
        result.msg = "fail"
    return result


@strawberry.mutation(description="Deletes a document")
async def document_delete(
    self, info: strawberry.types.Info, document: DocumentUpdateGQLModel
) -> DocumentResultGQLModel:
    loader = getLoaders(info).documents
    result = DocumentResultGQLModel()
    rows = await loader.filter_by(dspace_id=document.dspace_id)
    row = next(rows, None)

    if row is not None:
        row = await loader.delete(row.id)
        result.msg = "ok"
    else:
        result.id = None
        result.msg = "fail"
    return result