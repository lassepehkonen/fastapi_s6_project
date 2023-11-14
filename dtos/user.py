from typing import List, Optional

from pydantic import BaseModel

from dtos.auth import AccountResponse


class UpdateRole(BaseModel):
    roles_id: int


class UpdateUser(BaseModel):
    username: str


class UpdateUserPassword(BaseModel):
    password: str


class UsersResponse(BaseModel):
    items: List[AccountResponse]

