import strawberry
import datetime
import uuid
from typing import Union, Optional, List, Annotated, Any, Dict
import gql_documents.GraphTypeDefinitions
from DspaceAPI.Reguests import (
    login,
    createWorkspaceItem,
    addItemTitle,
    updateItemTitle,
    getItem,
    addBundleItem,
    getBundleId,
    addBitstreamsItem,
    getBitstreamItem,
    downloadItemContent,
)
from icecream import ic

def getLoaders(info):
    return info.context["all"]


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
    def author(self) -> uuid.UUID:
        # sync method which returns Awaitable :)
        return self.author

    @strawberry.field(description="""DSpace id""")
    def dspace_id(self) -> uuid.UUID:
        return self.dspace_id


@strawberry.input()
class DocumentInsertGQLModel:
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
    description: Optional[str] = strawberry.field(
        default=None, description="Brief description of document"
    )
    name: str = strawberry.field(default="Name", description="Document name")
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

    dspace_response: str = strawberry.field(
        default=None, description="""DSPACE response JSON to DICT"""
    )

    @strawberry.field(description="""Result of drone operation""")
    async def document(
        self, info: strawberry.types.Info
    ) -> Union[DocumentGQLModel, None]:
        result = await DocumentGQLModel.resolve_reference(info, self.id)
        return result


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
) -> Optional[DocumentResultGQLModel]:
    result = DocumentResultGQLModel()
    document = await DocumentGQLModel.resolve_reference(info, id)

    response_json = await getItem(document.dspace_id)
    result.dspace_response = str(response_json)

    if result.dspace_response is None:
        result.msg = "Fail"
        result.id = None

    else:
        result.msg = "Ok"
        result.id = id

    return result


#####################################################################
#
# Mutation section
#
#####################################################################


@strawberry.mutation(description="Defines a new document")
async def document_insert(
    self, info: strawberry.types.Info, document: DocumentInsertGQLModel
) -> DocumentResultGQLModel:
    loader = getLoaders(info).documents
    result = DocumentResultGQLModel()

    # DSpace reguest to create an item and returns its uuid
    dspaceID = await createWorkspaceItem()

    # if dspaceID.get("status") != 201:
    #     result.msg = dspaceID.get("message")
    #     result.id = None

    #     return result

    dspaceID = dspaceID.get("_embedded").get("item").get("uuid")
    document.dspace_id = dspaceID

    # DSPACE API reguest to add title and name it
    dspace_result = await addItemTitle(itemsId=dspaceID, titleName=document.name)

    dspace_bundle = await addBundleItem(itemsId=dspaceID)
    dspace_bundle = dspace_bundle.get("uuid")
    print("dspace bundle", dspace_bundle)

    # rows = await loader.filter_by(id=document.id)
    # row = next(rows, None)

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

    # DSPACE API reguest to update item name/title
    if document.name != None:
        newName = document.name
        document = await DocumentGQLModel.resolve_reference(info, document.id)
        document.name = newName
        response_status = await updateItemTitle(
            document.dspace_id, newName
        )
        
    # DSPACE API reguest to update description
    # if document.name != None:
    #     newName = document.name
    #     document = await DocumentGQLModel.resolve_reference(info, document.id)
    #     document.name = newName
    #     response_status = await updateItemTitle(
    #         document.dspace_id, newName
    #     )
        
        
        
        

    result = DocumentResultGQLModel()
    row = await loader.update(document)
    if row is None:
        result.id = None
        result.msg = f"fail, {response_status}"
    else:
        result.id = row.id
        result.msg = f"ok, {response_status}"

    return result


@strawberry.mutation(description="Add bitstream to dpsace")
async def dspace_add_bitstream(
    self, info: strawberry.types.Info, document: DocumentUpdateGQLModel
) -> DocumentResultGQLModel:
    loader = getLoaders(info).documents
    result = DocumentResultGQLModel()
    
    document = await DocumentGQLModel.resolve_reference(info, document.id)
    
    #get budle id
    response_json = await getBundleId(document.dspace_id)
    bundlesId = response_json["_embedded"]["bundles"][0]["uuid"]
    
    #add bitstream to that bundle
    response_status = await addBitstreamsItem(bundlesId)
    
    row = await loader.update(document)
    result.id = row.id

    if response_status == 201:
        result.msg = "ok"
        
    elif response_status == 400:
        result.msg = "Bad Request"
        
    elif response_status == 401:
        result.msg = "Unauthorized"
    
    elif response_status == 403:
        result.msg = "Forbidden"

    elif response_status == 404:
            result.msg = "Not found"

    return result



@strawberry.mutation(description="Get bitstream from dpsace")
async def dspace_get_bitstream(
    self, info: strawberry.types.Info, document: DocumentUpdateGQLModel
) -> DocumentResultGQLModel:
    loader = getLoaders(info).documents
    result = DocumentResultGQLModel()
    
    document = await DocumentGQLModel.resolve_reference(info, document.id)
    
    
    #get budle id WARNING: HARDCODED [0] its a list!
    response_json = await getBundleId(document.dspace_id)
    bundlesId = response_json["_embedded"]["bundles"][0]["uuid"]
    
    
    response_json = await getBitstreamItem(bundlesId)
    bitstreamId = response_json["_embedded"]["bitstreams"][0]["uuid"]
    bitstreamName = response_json["_embedded"]["bitstreams"][0]["name"]


    #add bitstream to that bundle
    response_status = await downloadItemContent(bitstreamId, bitstreamName)

    row = await loader.update(document)
    
    result.id = row.id
    if response_status == 200:
        result.msg = "ok"
            
    elif response_status == 204:
        result.msg = "No Content"
        
    elif response_status == 401:
        result.msg = "Unauthorized"
    
    elif response_status == 403:
        result.msg = "Forbidden"

    elif response_status == 404:
        result.msg = "Not found"
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
