
from pydantic import BaseModel


class Role(BaseModel):
    id: int
    name: str


class UserLoginRes(BaseModel):
    access_token: str
    refresh_token: str
    csrf_token: str


class UserRegisterRequest(BaseModel):
    username: str
    password: str


class UserRegisterResponse(BaseModel):
    id: int
    username: str
    role: Role


class AccountResponse(BaseModel):
    id: int
    username: str
    role: Role


class SessionData(BaseModel):
    data: str

