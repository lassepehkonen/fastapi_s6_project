import os
from typing import Annotated, Optional

from fastapi import Depends, Cookie, HTTPException
from fastapi.security import OAuth2PasswordBearer

import models
from dtos.auth import SessionData
from tokens.session import AuthResponseHandlerSession, verifier
from tokens.token import AuthResponseHandlerToken, Token
from services.auth_service import AuthService
from tokens.base import AuthResponseHandlerBase

auth_type = os.getenv('AUTH_TYPE')

oauth_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False)

Oauth = Annotated[Optional[str], Depends(oauth_scheme)]
Token_cookie = Annotated[Optional[str], Cookie()]
verifier_cookie = Annotated[Optional[SessionData], Depends(verifier)]


class AuthRequiredHandlerBase:
    def verify(self, _token: Token, service: AuthService, authorization: Oauth = None,
               access_token_cookie: Token_cookie = None, _cookie: verifier_cookie = None):
        pass


class AuthRequiredHandlerToken(AuthRequiredHandlerBase):
    def verify(self, _token: Token, service: AuthService, authorization: Oauth = None,
               access_token_cookie: Token_cookie = None, _cookie: verifier_cookie = None):

        try:
            encoded = None
            if access_token_cookie is not None:
                encoded = access_token_cookie
            else:
                if authorization is not None:
                    encoded = authorization
            if encoded is None:
                raise HTTPException(status_code=401, detail='unauthorized')
            claims = _token.validate(encoded)
            if claims['type'] != 'access':
                raise HTTPException(status_code=401, detail='access token required')
            user = service.get_account_by_access_token(claims['sub'])
            if user is None:
                raise HTTPException(status_code=401, detail='unauthorized')
            return user

        except Exception as e:
            raise HTTPException(status_code=401, detail='unauthorized')


class AuthRequiredHandlerSession(AuthRequiredHandlerBase):
    def verify(self, _token: Token, service: AuthService, authorization: Oauth = None,
               access_token_cookie: Token_cookie = None, _cookie: verifier_cookie = None):

        try:
            if _cookie is None:
                raise HTTPException(status_code=401, detail='Unauthorized')

            user = service.get_account_by_access_token(_cookie.data)
            if user is None:
                raise HTTPException(status_code=401, detail='Unauthorized')

            return user

        except Exception as e:
            raise HTTPException(status_code=401, detail='unauthorized')


def init_auth_res():
    if auth_type == 'session':
        return AuthResponseHandlerSession()
    else:
        return AuthResponseHandlerToken()


def init_auth_handler():
    if auth_type == 'session':
        return AuthRequiredHandlerSession()
    else:
        return AuthRequiredHandlerToken()


AccountHandler = Annotated[AuthRequiredHandlerBase, Depends(init_auth_handler)]


def get_logged_in_user(_token: Token, service: AuthService, account_handler: AccountHandler,
                       authorization: Oauth = None, access_token_cookie: Token_cookie = None,
                       _cookie: verifier_cookie = None):
    return account_handler.verify(_token, service, authorization, access_token_cookie, _cookie)


async def get_refresh_token(_token: Token, service: AuthService, authorization: Oauth = None,
                            refresh_token_cookie: Token_cookie = None):
    try:
        encoded = None
        if refresh_token_cookie is not None:
            encoded = refresh_token_cookie
        else:
            if authorization is not None:
                encoded = authorization
        if encoded is None:
            raise HTTPException(status_code=401, detail='Unauthorized')
        claims = _token.validate(encoded)
        if claims['type'] != 'refresh':
            raise HTTPException(status_code=401, detail='Refresh token required')
        user = service.get_account_by_refresh_token(claims['sub'])
        if user is None:
            raise HTTPException(status_code=401, detail='Unauthorized')
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail='Unauthorized')


LoggedInUser = Annotated[models.User, Depends(get_logged_in_user)]


def require_admin(account: LoggedInUser):
    if account.role == 'admin':
        return account
    raise HTTPException(status_code=403, detail='forbidden')


def require_staff(account: LoggedInUser):
    if account.role == 'admin' or account.role == 'teacher':
        return account
    raise HTTPException(status_code=403, detail='forbidden')


RefreshableUser = Annotated[models.User, Depends(get_refresh_token)]

Admin = Annotated[models.User, Depends(require_admin)]
Staff = Annotated[models.User, Depends(require_staff)]

AuthRes = Annotated[AuthResponseHandlerBase, Depends(init_auth_res)]
