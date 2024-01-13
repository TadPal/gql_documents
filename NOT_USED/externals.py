import strawberry
import uuid


@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
    return cls(id=id)


class BaseEternal:
    id: uuid.UUID = strawberry.federation.field(external=True)


@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference


@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference
