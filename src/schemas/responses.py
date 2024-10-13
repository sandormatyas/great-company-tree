from pydantic import BaseModel, UUID4, Field


class CompanyUnit(BaseModel):
    id: UUID4
    parent_id: UUID4 | None
    root_id: UUID4
    height: int

    name: str
    children: list["CompanyUnit"] = Field(default_factory=list)
