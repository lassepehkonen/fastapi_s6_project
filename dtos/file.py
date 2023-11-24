from pydantic import BaseModel


class File(BaseModel):
    id: int
    original_name: str
    random_name: str
