from pydantic import BaseModel, UUID4, Field


class CompanyUnitResponse(BaseModel):
    id: UUID4
    parent_id: UUID4 | None
    root_id: UUID4
    height: int

    name: str
    children: list["CompanyUnitResponse"] = Field(default_factory=list)
