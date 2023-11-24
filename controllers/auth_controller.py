import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import Response

from dtos.auth import UserLoginRes, UserRegisterResponse, AccountResponse, UserRegisterRequest
import tokens.token
from dependencies import LoggedInUser, RefreshableUser, AuthRes

from services.auth_service import AuthService
from tokens.session import cookie


router = APIRouter(prefix='/api/v1/auth', tags=['Authorize'])

LoginForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/register', response_model=UserRegisterResponse)
def register(req: UserRegisterRequest, service: AuthService):
    user = service.register(req)
    return user


@router.get('/account', dependencies=[Depends(cookie)], response_model=AccountResponse)
def get_account(account: LoggedInUser):
    return account


@router.post('/refresh', response_model=UserLoginRes)
async def refresh(service: AuthService, _token: tokens.token.Token, account: RefreshableUser, res: Response):
    csrf = str(uuid.uuid4())
    _tokens = service.refresh(_token, csrf, account)
    res.set_cookie("access_token_cookie", _tokens['access_token'], secure=True, httponly=True,
                   samesite="strict")

    res.set_cookie("csrf_token_cookie", _tokens['csrf_token'], secure=True, httponly=True,
                   samesite="strict")
    _tokens['refresh_token'] = ''

    return _tokens


@router.post('/login', response_model=UserLoginRes)
async def login(service: AuthService, login_form: LoginForm, _token: tokens.token.Token, res: Response,
                res_handler: AuthRes):
    csrf = str(uuid.uuid4())
    _tokens = service.login(login_form.username, login_form.password, csrf, _token)
    if _tokens is None:
        raise HTTPException(status_code=404, detail='User not found')
    return await res_handler.send(res, _tokens['access_token'], _tokens['refresh_token'], _tokens['csrf_token'],
                                  _tokens['sub'])


@router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(service: AuthService, res: Response, session_id: Annotated[uuid.UUID, Depends(cookie)],
                 account: LoggedInUser, res_handler: AuthRes):
    service.logout(account.access_token_identifier)
    await res_handler.logout(session_id, res)
    return None

