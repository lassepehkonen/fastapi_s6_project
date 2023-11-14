
from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

import models
from controllers import user_controllers
from controllers.auth_controllers import get_current_user, logout_controller, refresh_access_token_controller, \
    login_for_access_token_controller
from controllers.user_controllers import get_users_controller, get_user_by_id_controller, create_user_controller, \
    update_user_password_controller
from controllers.viewing_controllers import get_viewings_controller, get_viewing_by_id_controller, \
    create_new_viewing_controller, accept_viewing_controller

from schemas import (ViewingsBase, ViewingSchema, ViewingCreate, CreateUserRequest, Token, UsersBase, UserSchema,
                     PasswordUpdate, LoginResponse, ViewingUpdate)

router = APIRouter()




@router.get("/api/v1/viewings", status_code=status.HTTP_200_OK, response_model=ViewingsBase)
async def get_viewings(db: db_dependency):
    return get_viewings_controller(db)


@router.get('/api/v1/viewings/{viewing_id}', status_code=status.HTTP_200_OK, response_model=ViewingSchema)
def get_viewing_by_id(viewing_id: int, db: db_dependency):
    return get_viewing_by_id_controller(viewing_id, db)


@router.post("/api/v1/viewings/create_viewing")
async def create_new_viewing(current_user: user_dependency, viewing_data: ViewingCreate, db: db_dependency):
    return create_new_viewing_controller(current_user, viewing_data, db)


@router.put("/api/v1/viewings/{viewing_id}/accept", response_model=ViewingUpdate)
async def accept_viewing(db: db_dependency, viewing_id: int, current_user: user_dependency):
    return accept_viewing_controller(viewing_id, current_user, db)




