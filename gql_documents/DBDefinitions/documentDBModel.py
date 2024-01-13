import sqlalchemy
from sqlalchemy import Column, String, DateTime, Uuid
from .UUID import UUIDColumn
from .Base import BaseModel


class DocumentModel(BaseModel):
    __tablename__ = "documents"

    id = UUIDColumn()
    dspace_id = Column(Uuid, index=True)

    name = Column(String)
    author_id = Column(Uuid, index=True, nullable=True)
    description = Column(String, comment="Brief description of the document")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
