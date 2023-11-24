
from pydantic import BaseModel


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
    role: str


class AccountResponse(BaseModel):
    id: int
    username: str
    role: str


class SessionData(BaseModel):
    data: str

