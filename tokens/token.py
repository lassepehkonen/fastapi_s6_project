import time
import uuid
from typing import Annotated
import jwt
from fastapi import Depends
from starlette.responses import Response

from tokens.base import AuthResponseHandlerBase


class TokenInterface:
    def create(self, claims):
        pass

    def validate(self, t):
        pass


class AsymmetricToken(TokenInterface):
    def __init__(self):
        with open('cert/id_rsa') as f:
            self.private = f.read()

        with open('cert/id_rsa.pub') as f:
            self.public = f.read()

    def create(self, sub, _type, csrf):
        now = time.time()
        data = {'sub': sub,
                'iss': 's6backend',
                'aud': 'localhost',
                'type': _type,
                'exp': now + 3600, 'nbf': now - 500, 'iat': now}
        if _type == 'access':
            data['csrf'] = csrf
        if _type == 'refresh':
            data['exp'] = now + 3600 * 24
        _token = jwt.encode(data,
                                  self.private,
                                  algorithm="RS512")

        return _token

    def validate(self, t):
        claims = jwt.decode(t, self.public, 'RS512', audience='localhost')
        return claims


def init_token():
    return AsymmetricToken()


Token = Annotated[TokenInterface, Depends(init_token)]


class AuthResponseHandlerToken(AuthResponseHandlerBase):
    async def send(self, res: Response, access: str, refresh: str, csrf: str, sub: str):
        res.set_cookie("access_token_cookie", access, samesite="strict")
        res.set_cookie("refresh_token_cookie", refresh, samesite="strict")
        res.set_cookie("csrf_token_cookie", csrf, samesite="strict")

        return {'access_token': access, 'refresh_token': refresh, 'csrf_token': csrf}

    async def logout(self, session_id: uuid.UUID, res: Response):
        res.delete_cookie('access_token_cookie')
        res.delete_cookie('refresh_token_cookie')
        res.delete_cookie('csrf_token_cookie')

