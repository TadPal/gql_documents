import pytest
import logging
import uuid
import sqlalchemy
from gql_documents.GraphTypeDefinitions import schema
from tests.shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    createContext,
)


def createByIdTest(tableName, queryEndpoint, attributeNames=["id"]):
    attlist = " ".join(attributeNames)

    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        assert data.get(tableName, None) is not None
        datatable = data[tableName]
        assert len(datatable) > 0
        datarow = data[tableName][0]

        query = "query($id: UUID!){" f"{queryEndpoint}(id: $id)" "{" + attlist + "}}"

        context_value = await createContext(async_session_maker)

        datarow["id"] = str(datarow["id"])
        variable_values = {"id": datarow["id"]}

        resp = await schema.execute(
            query, context_value=context_value, variable_values=variable_values
        )
        assert resp.errors is None

        respdata = resp.data[queryEndpoint]

        assert respdata is not None

        for att in attributeNames:
            assert respdata[att] == datarow[att]

    return result_test


def createPageTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()

        query = "query{" f"{queryEndpoint}" "{ id, name }}"

        context_value = await createContext(async_session_maker)
        resp = await schema.execute(query, context_value=context_value)
        assert resp.errors is None

        respdata = resp.data[queryEndpoint]
        datarows = data[tableName]

        for datarow in datarows:
            datarow["id"] = str(datarow["id"])

        for rowa, rowb in zip(respdata, datarows):
            for att in attributeNames:
                assert rowa[att] == rowb[att]

    return result_test


def createResolveReferenceTest(tableName, gqltype, attributeNames=["id", "name"]):
    attlist = " ".join(attributeNames)

    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        table = data[tableName]
        for row in table:
            rowid = row["id"]

            query = (
                "query { _entities(representations: [{ __typename: "
                + f'"{gqltype}", id: "{rowid}"'
                + " }])"
                + "{"
                + f"...on {gqltype}"
                + "{"
                + attlist
                + "}"
                + "}"
                + "}"
            )

            context_value = await createContext(async_session_maker)
            resp = await schema.execute(query, context_value=context_value)
            data = resp.data
            data = data["_entities"][0]
            if isinstance(data["id"], str):
                data["id"] = uuid.UUID(data["id"])
            assert data["id"] == rowid

    return result_test
