from uuid import uuid4
from sqlalchemy import Column, Uuid

uuid = uuid4


def UUIDColumn():
    return Column(Uuid, primary_key=True, comment="primary key", default=uuid)


# def UUIDFKey(comment=None, nullable=True, **kwargs):
#     return Column(Uuid, index=True, nullable=nullable, **kwargs)
