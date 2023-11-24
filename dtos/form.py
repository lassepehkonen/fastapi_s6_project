import datetime
from typing import Optional, List

from pydantic import BaseModel

from dtos.environment import Envinronment
from dtos.file import File
from dtos.inspection_type import InspectionType
from dtos.target import Target
from dtos.user import User


class Form(BaseModel):
    id: int
    createdAt: datetime.datetime
    closedAt: Optional[datetime.datetime] = None
    user: User
    environment: Optional[Envinronment] = None
    inspectiontarget: Optional[Target] = None
    inspectiontype: InspectionType
    files: List[File]


class FormRes(BaseModel):
    form: Form