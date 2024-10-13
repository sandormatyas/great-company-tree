from pydantic import BaseModel, UUID4


class NodeCreate(BaseModel):
    name: str
    height: int
