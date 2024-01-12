import pytest

from .gt_utils import (
    createByIdTest,
    createPageTest,
    createResolveReferenceTest,
    createFrontendQuery,
    createUpdateQuery,
)


test_reference_documents = createResolveReferenceTest(
    tableName="documents",
    gqltype="DocumentsGQLModel",
    attributeNames=["id", "name", "lastchange", "dspace_id", "author", "description"],
)
test_query_form_by_id = createByIdTest(
    tableName="documents", queryEndpoint="documentById"
)
test_query_form_page = createPageTest(
    tableName="documents", queryEndpoint="documentPage"
)

test_document_insert = createFrontendQuery(
    query="""
    mutation($name: String!, $author: UUID!, $description: String!) { 
        result: documentInsert(document: {name: $name, description: $description, author: $author}) { 
            id
            msg
            document {
                id
                name
                author
                description
                dspace_id
                lastchange
                created           
            }
        }
    }
    """,
    variables={
        "name": "new Doc",
        "author": "89d1f3cc-ae0f-11ed-9bd8-0242ac110002",
        "description": "Sample description",
    },
    asserts=[],
)

test_document_update = createUpdateQuery(
    query="""
    mutation($id: UUID!, $name: String!, $author: UUID!, $description: String!, $lastchange: DateTime!) { 
        result: documentInsert(document: {name: $name, description: $description, author: $author, lastchange: $lastchange}) { 
            id
            msg
            document {
                id
                name
                author
                description
                dspace_id
                lastchange
                created           
            }
        }
    }
    """,
    variables={
        "id": "e5d5286d-50d2-4b07-97de-7407c62c21c1",
        "name": "Pytest name",
        "author": "89d1f3cc-ae0f-11ed-9bd8-0242ac110002",
        "description": "Sample description",
    },
    tableName="documents",
)
