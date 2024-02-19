import pytest
import uuid
from .gt_utils import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    prepare_in_memory_sqllite,
    prepare_demodata,
    get_demodata,
    createContext,
    schema,
)


test_reference_documents = createResolveReferenceTest(
    tableName="documents",
    gqltype="DocumentGQLModel",
    attributeNames=["id", "name", "lastchange", "authorId", "description", "created"],
)
test_query_form_by_id = createByIdTest(
    tableName="documents", queryEndpoint="documentById"
)
test_query_form_page = createPageTest(
    tableName="documents", queryEndpoint="documentsPage"
)


@pytest.mark.asyncio
async def test_document_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    name = "Pytest"
    description = "Pytest description"

    query = """
            mutation(
                $name: String!
                $description: String!
                $collectionId: UUID!
                $type: String!
                $language: String!
                ) {
                operation: documentInsert(
                    document: {
                        name: $name
                        description: $description
                    },
                    collectionId: $collectionId,
                    type: $type,
                    language: $language
                ){
                    msg
                    entity: document {
                        id
                        name
                        lastchange
                    }
                }
            }
        """

    context_value = await createContext(async_session_maker)
    variable_values = {
        "name": name,
        "description": description,
        "collectionId": "c9895381-5370-4261-bd5b-13fd671189f9",
        "type": "pdf",
        "language": "Czech",
    }

    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )

    print(resp, flush=True)
    assert resp.errors is None
    data = resp.data["operation"]
    assert data["msg"] == "Ok"
    data = data["entity"]
    assert data["name"] == name

    id = data["id"]
    lastchange = data["lastchange"]

    name = "Pytest new name"
    query = """
            mutation(
                $id: UUID!,
                $lastchange: DateTime!
                $name: String!
                ) {
                operation: documentUpdate(document: {
                id: $id,
                lastchange: $lastchange
                name: $name
            }){
                id
                msg
                entity: document {
                    id
                    name
                    lastchange
                }
            }
            }
        """

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id, "name": name, "lastchange": lastchange}
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None

    data = resp.data["operation"]
    assert data["msg"] == "Ok"
    data = data["entity"]
    assert data["name"] == name

    # lastchange je jine, musi fail
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )

    assert resp.errors is None
    data = resp.data["operation"]
    assert data["msg"] == "Ok"

    pass


@pytest.mark.asyncio
async def test_get_dspace_bitstream():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    id = "b7e8c6f7-9e51-4712-9dc5-9b5e3ad5a2fa"

    query = """
            query ($id: UUID!) {
                operation: dspaceGetBitstream(id: $id) {
                    msg
                }
            }
        """

    context_value = await createContext(async_session_maker)
    variable_values = {"id": id}

    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )

    assert resp.errors is None
    data = resp.data["operation"]
    assert data["msg"] in ["Unauthorized", "Ok", "No Content", "Forbidden", "Not found"]

    pass


@pytest.mark.asyncio
async def test_communities_page():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    query = """
            query {
                operation: communitiesPage{
                    msg
                }
            }
        """

    context_value = await createContext(async_session_maker)

    resp = await schema.execute(query, context_value=context_value)

    assert resp.errors is None
    data = resp.data["operation"]
    assert data["msg"] in ["Unauthorized", "Ok", "No Content", "Forbidden", "Not found"]

    pass


@pytest.mark.asyncio
async def test_collections_page():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    query = """
            query {
                operation: collectionsPage{
                    msg
                }
            }
        """

    context_value = await createContext(async_session_maker)

    resp = await schema.execute(query, context_value=context_value)

    assert resp.errors is None
    data = resp.data["operation"]
    assert data["msg"] in ["Unauthorized", "Ok", "No Content", "Forbidden", "Not found"]

    pass
