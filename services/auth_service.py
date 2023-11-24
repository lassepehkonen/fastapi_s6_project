import time
import uuid
from typing import Optional, Annotated, Any, Union

from fastapi import Depends
from passlib.context import CryptContext

import dtos.auth
from models import db_dependency, User
from tokens.token import Token

from services.base_service import BaseService


def get_auth_service(db: db_dependency):
    return AuthAlchemyService(db)


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class AuthAlchemyService(BaseService):
    def __init__(self, db: db_dependency):

        super(AuthAlchemyService, self).__init__(db)

    def register(self, req: dtos.auth.UserRegisterRequest) -> User:
        user = User(**req.model_dump())
        user.password = bcrypt_context.hash(user.password)
        user.role = 'user'
        self.db.add(user)
        self.db.commit()
        return user

    def get_account_by_refresh_token(self, sub: str):
        user = self.db.query(User).filter(User.refresh_token_identifier == sub).first()
        if user is not None:
            return user
        return None

    def get_account_by_access_token(self, sub: str):
        user = self.db.query(User).filter(User.access_token_identifier == sub).first()
        if user is not None:
            return user
        return None

    def logout(self, sub):
        user = self.get_account_by_access_token(sub)
        user.access_token_identifier = None
        user.refresh_token_identifier = None
        self.db.commit()

    def refresh(self, _token: Token, csrf: str, account: User):
        access_identifier = str(uuid.uuid4())
        access_token = _token.create(access_identifier, 'access', csrf)
        csrf_token = _token.create(csrf, 'csrf', None)
        account.access_token_identifier = access_identifier
        self.db.commit()

        return {'access_token': access_token, 'csrf_token': csrf_token, 'sub': access_identifier}

    def login(self, username: str, password: str, csrf: str, _token: Token,):
        user = self.db.query(User).filter(User.username == username).first()
        if user is None:
            return None
        valid = bcrypt_context.verify(password, user.password)
        if not valid:
            return None
        now = time.time()
        access_identifier = str(uuid.uuid4())
        refresh_identifier = str(uuid.uuid4())
        access_token = _token.create(access_identifier, 'access', csrf)
        refresh_token = _token.create(refresh_identifier, 'refresh', None)
        csrf_token = _token.create(csrf, 'csrf', None)

        user.refresh_token_identifier = refresh_identifier
        user.access_token_identifier = access_identifier
        self.db.commit()

        return {'access_token': access_token, 'refresh_token': refresh_token, 'csrf_token': csrf_token,
                'sub': access_identifier}


AuthService = Annotated[AuthAlchemyService, Depends(get_auth_service)]

