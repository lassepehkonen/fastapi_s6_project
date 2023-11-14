import datetime
from typing import List, Optional

from pydantic import BaseModel


# Viewing Schemas here!
# ViewingBase inherits into other viewing classes


class ViewingBase(BaseModel):
    what_positive: str
    what_negative: str
    observations: str
    improvement_idea: str
    photo: Optional[bytes] = None
    grade: int


class ViewingCreate(ViewingBase):
    pass


class ViewingUpdate(BaseModel):
    accepted: bool


class ViewingSchema(ViewingBase):
    id: int
    create_date: datetime.date
    accepted: bool


class ViewingsBase(BaseModel):
    items: List[ViewingSchema]

