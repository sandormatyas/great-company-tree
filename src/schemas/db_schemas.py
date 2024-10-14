from pydantic import BaseModel, UUID4


class EdgeUpdate(BaseModel):
    parent_id: UUID4 | None = None
    child_id: UUID4 | None = None
    weight: int | None = None
