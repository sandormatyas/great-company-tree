from pydantic import BaseModel, UUID4


class CompanyUnitCreate(BaseModel):
    parent_id: UUID4 | None

    name: str


class CompanyUnitUpdate(BaseModel):
    parent_id: UUID4
