import uuid

from sqlalchemy import Column, Integer, String, Uuid, ForeignKey
from src.database import Base


class CompanyUnit(Base):
    __tablename__ = "company_units"

    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4, unique=True)
    height = Column(Integer)

    name = Column(String)  # helping readability


class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True, unique=True)
    parent_id = Column(Uuid, ForeignKey("company_units.id"))
    child_id = Column(Uuid, ForeignKey("company_units.id"))
    weight = Column(Integer)
