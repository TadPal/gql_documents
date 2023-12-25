import strawberry
import datetime
import uuid
from typing import Union, Optional, List, Annotated
import gql_documents.GraphTypeDefinitions
from DspaceAPI.Reguests import (
    login,
    createWorkspaceItem,
    addItemTitle,
    updateItemTitle,
    getItem,
)


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
    def id(self) -> uuid.UUID:
        return self.id

    @strawberry.field(description="""Brief description""")
    def description(self) -> Optional[str]:
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
    def dspace_id(self) -> uuid.UUID:
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
    self, info: strawberry.types.Info, id: uuid.UUID
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
    dspace_id: uuid.UUID = strawberry.field(
        default=None, description="Primary key of dspace entity"
    )
    description: Optional[str] = strawberry.field(
        default=None, description="Brief description of document"
    )
    name: str = strawberry.field(default="Name", description="Document name")
    author: Optional[uuid.UUID] = strawberry.field(
        default=None, description="ID of Author"
    )


@strawberry.input()
class DocumentUpdateGQLModel:
    id: uuid.UUID = strawberry.field(default=None, description="Primary key")
    lastchange: datetime.datetime = strawberry.field(
        default=None, description="Timestamp"
    )
    dspace_id: Optional[uuid.UUID] = strawberry.field(
        default=None, description="Primary key of dspace entity"
    )
    description: Optional[str] = strawberry.field(
        default=None, description="Brief description of document"
    )
    name: Optional[str] = strawberry.field(default="Name", description="Document name")
    author: Optional[uuid.UUID] = strawberry.field(
        default=None, description="ID of Author"
    )


@strawberry.type()
class DocumentResultGQLModel:
    id: Optional[uuid.UUID] = strawberry.field(
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


@strawberry.mutation(description="Defines a new document")
async def document_insert(
    self, info: strawberry.types.Info, document: DocumentInsertGQLModel
) -> DocumentResultGQLModel:
    loader = getLoaders(info).documents

    # DSpace reguest to create an item and returns its uuid
    dspaceID = await createWorkspaceItem(name=document.name)
    dspaceID = dspaceID.get("_embedded").get("item").get("uuid")
    document.dspace_id = dspaceID

    # DSPACE API reguest to add title and name it
    dspace_result = await addItemTitle(itemsId=dspaceID, titleName=document.name)
    if dspace_result is not None:
        print(dspace_result)

    result = DocumentResultGQLModel()
    rows = await loader.filter_by(id=document.dspace_id)
    row = next(rows, None)

    if row is None:
        row = await loader.insert(document)
        result.id = row.id
        result.msg = "ok"
    else:
        result.id = row.id
        result.msg = "fail"
    return result


@strawberry.mutation(description="Update existing document")
async def document_update(
    self, info: strawberry.types.Info, document: DocumentUpdateGQLModel
) -> DocumentResultGQLModel:
    loader = getLoaders(info).documents

    # DSPACE API reguest to update item title
    dspace_result = await updateItemTitle(
        itemsId=document.dspace_id, titleName=document.name
    )
    if dspace_result is not None:
        print(dspace_result)

    result = DocumentResultGQLModel()
    row = await loader.update(document)
    if row is None:
        result.id = None
        result.msg = "fail"
    else:
        result.id = row.id
        result.msg = "ok"

    return result


@strawberry.mutation(description="Deletes a document")
async def document_delete(
    self, info: strawberry.types.Info, document: DocumentUpdateGQLModel
) -> DocumentResultGQLModel:
    loader = getLoaders(info).documents
    result = DocumentResultGQLModel()
    rows = await loader.filter_by(id=document.id)
    row = next(rows, None)

    if row is not None:
        row = await loader.delete(row.id)
        result.msg = "ok"
    else:
        result.id = None
        result.msg = "fail"
    return result
