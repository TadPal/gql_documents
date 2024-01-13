import pytest

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
    attributeNames=["id", "name", "lastchange", "authorId", "description"],
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
                ) {
                operation: documentInsert(document: {
                    name: $name
                    description: $description
                }){
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
    variable_values = {"name": name, "description": description}

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
                $id: ID!,
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
    newName = "Pytest new name"
    context_value = await createContext(async_session_maker)
    variable_values = {"id": id, "name": newName, "lastchange": lastchange}
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None

    data = resp.data["operation"]
    assert data["msg"] == "ok"
    data = data["entity"]
    assert data["name"] == newName

    # lastchange je jine, musi fail
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None
    data = resp.data["operation"]
    assert data["msg"] == "fail"

    pass
