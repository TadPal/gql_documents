from uoishelpers.dataloaders import createIdLoader
from functools import cache

from gql_documents.DBDefinitions import (
    DocumentModel,
)


async def createLoaders(asyncSessionMaker):
    class Loaders:
        @property
        @cache
        def documents(self):
            return createIdLoader(asyncSessionMaker, DocumentModel)

    return Loaders()


def createLoadersContext(asyncSessionMaker):
    return {"loaders": createLoaders(asyncSessionMaker)}
