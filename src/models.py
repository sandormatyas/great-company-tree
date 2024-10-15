import uuid

from sqlalchemy import Column, Integer, String, Uuid, ForeignKey
from src.database import Base


class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True, unique=True)
    parent_id = Column(Uuid, ForeignKey("nodes.id"))
    child_id = Column(Uuid, ForeignKey("nodes.id"))
    depth = Column(Integer)


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4, unique=True)
    name = Column(String)  # helping readability
