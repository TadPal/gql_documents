import sqlalchemy
import sys
import asyncio
import pytest

from gql_documents.GraphTypeDefinitions import schema
from .shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    createContext,
)
from typing import List


@pytest.mark.asyncio
async def test_external_ids():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data["externalids"]
    row = table[0]
    query = """query($id: ID!){
        externalIds(innerId: $id ) { 
            id
            innerId
            outerId
        }
    }"""

    variable_values = {"id": row["inner_id"]}
    context_value = await createContext(async_session_maker)
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    print(resp, flush=True)

    # respdata = resp.data['eventById']
    assert resp.errors is None

    data = resp.data

    assert data["externalIds"][0]["innerId"] == row["inner_id"]
    assert data["externalIds"][0]["outerId"] == row["outer_id"]


@pytest.mark.asyncio
async def test_internal_ids():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data["externalids"]
    row = table[0]
    print(row, flush=True)
    query = """query($id: String! $type_id: ID!){
        internalId(outerId: $id typeidId: $type_id) }"""

    variable_values = {"id": row["outer_id"], "type_id": row["typeid_id"]}
    context_value = await createContext(async_session_maker)
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )

    assert resp.errors is None
    data = resp.data
    print(data, flush=True)

    assert data["internalId"] == row["inner_id"]


@pytest.mark.asyncio
async def test_representation_externalid():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    id = data["externalids"][0]["id"]

    query = """
            query($id: ID!) {
                _entities(representations: [{ __typename: "ExternalIdGQLModel", id: $id }]) {
                    ...on ExternalIdGQLModel {
                        id
                        innerId
                        outerId
                    }
                }
            }
        """
    variable_values = {"id": id}
    context_value = await createContext(async_session_maker)
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )

    print(resp, flush=True)
    respdata = resp.data["_entities"]
    assert respdata[0]["id"] == id
    assert resp.errors is None


@pytest.mark.asyncio
async def test_group_add_external_id():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data["groups"]
    row = table[0]
    id = row["id"]

    query = """
            mutation(
                $inner_id: ID!
                $typeid_id: ID!
                $outer_id: ID!
            ) {
                result: externalidInsert(externalid: {
                    innerId: $inner_id
                    typeidId: $typeid_id
                    outerId: $outer_id
                }) {
                    id
                    msg
                    externalid {
                        id
                        innerId
                        outerId
                        idType {
                            id
                        }
                    }
                }
            }
        """

    context_value = await createContext(async_session_maker)
    variable_values = {
        "inner_id": id,
        "outer_id": "999",
        "typeid_id": data["externalidtypes"][0]["id"],
    }
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None

    respdata = resp.data
    result = respdata["result"]
    assert result["externalid"]["outerId"] == "999"
    assert result["externalid"]["innerId"] == id


@pytest.mark.asyncio
async def test_user_add_external_id():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data["groups"]
    row = table[0]
    id = row["id"]


##############################################################

from .creators import (
    createPageTest,
    createResolveReferenceTest,
    createResolveReferenceTestApp,
    createByIdTest,
)

test_externalidtype = createPageTest(
    "externalidtypes",
    "externalidtypePage",
    ["id", "name"],
    subEntities=["createdBy{ id }", "changedBy{ id }", "nameEn", "category{ id }"],
)
test_externalidcategory = createPageTest(
    "externalidcategories",
    "externalidcategoryPage",
    ["id", "name"],
    subEntities=["nameEn createdBy{ id }", "changedBy{ id }"],
)

test_externalidcategory_reference = createResolveReferenceTest(
    "externalidcategories", "ExternalIdCategoryGQLModel"
)
test_externalidtype_reference = createResolveReferenceTest(
    "externalidtypes", "ExternalIdTypeGQLModel", subEntities=["nameEn"]
)
test_externalid_reference = createResolveReferenceTest(
    "externalids", "ExternalIdGQLModel", ["id", "lastchange"], subEntities=["typeName"]
)

test_externaltypeid_byId = createByIdTest(
    "externalidtypes", "externalidtypeById", ["id", "name"]
)
# test_user_representation = createResolveReferenceTest("users", "UserGQLModel", ["id"])
# test_group_representation = createResolveReferenceTest("groups", "GroupGQLModel", ["id"])
