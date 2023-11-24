from pydantic import BaseModel


class Target(BaseModel):
    id: int
    name: str