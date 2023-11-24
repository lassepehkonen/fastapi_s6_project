from typing import List, Optional

from pydantic import BaseModel

from dtos.auth import AccountResponse


class User(BaseModel):
    id: int
    email: str


class UpdateRole(BaseModel):
    role: str


class UpdateUser(BaseModel):
    username: str


class UpdateUserPassword(BaseModel):
    password: str


class UsersResponse(BaseModel):
    items: List[AccountResponse]
