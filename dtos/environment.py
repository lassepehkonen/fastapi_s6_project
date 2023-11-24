from pydantic import BaseModel


class Envinronment(BaseModel):
    id: int
    name: str
