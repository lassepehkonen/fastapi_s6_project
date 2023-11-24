
from typing import Annotated

from fastapi import Depends

from dtos.user import UpdateRole, UpdateUserPassword
from models import db_dependency, User
from services.auth_service import bcrypt_context
from services.base_service import BaseService


def get_user_service(db: db_dependency):
    return UserUpdateService(db)


class UserUpdateService(BaseService):
    def __init__(self, db: db_dependency):

        super(UserUpdateService, self).__init__(db)

    def get_users(self):
        users = self.db.query(User).all()
        return users

    def get_user_by_id(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        return user

    def update_user_role(self, user_id: int, update: UpdateRole):
        user = self.get_user_by_id(user_id)
        if user is None:
            return None

        user.role = update.role

        self.db.commit()
        return True

    def update_user_password(self, user_id: int, update: UpdateUserPassword):
        user = self.get_user_by_id(user_id)
        if user is None:
            return None
        user.password = bcrypt_context.hash(update.password)
        self.db.commit()
        return True

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if user is None:
            return None
        del user
        self.db.commit()
        return True


UserService = Annotated[UserUpdateService, Depends(get_user_service)]

