import strawberry
from typing import List

from .documentGQLmodel import DocumentGQLModel


def getLoaders(info):
    return info.context["all"]


###########################################################################################################################
#
# zde definujte sve rozsirene GQL modely,
# ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
# venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
#
# vsimnete si,
# - jak je definovan dekorator tridy (extend=True)
# - jaky dekorator je pouzit (federation.type)
#
# - venujte pozornost metode resolve reference, tato metoda je dulezita pro komunikaci mezi prvky federace,
# - ma odlisnou implementaci v porovnani s modelem, za ktery jste odpovedni
#
###########################################################################################################################


@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        if id is None:
            return None
        return UserGQLModel(id=id)

    @strawberry.field(description="""All documents related to the user""")
    async def documents(self, info: strawberry.types.Info) -> List["DocumentGQLModel"]:
        loader = getLoaders(info=info).documents
        result = await loader.filter_by(author=self.id)
        return result


@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: strawberry.ID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberry.ID):
        return GroupGQLModel(id=id)

    @strawberry.field(description="""All documents related to a group""")
    async def documents(self, info: strawberry.types.Info) -> List["DocumentGQLModel"]:
        loader = getLoaders(info=info).documents
        result = await loader.filter_by(author=self.id)  # Change to group
        return result
