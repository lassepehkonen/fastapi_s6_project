from fastapi import HTTPException, APIRouter
from starlette import status

from dependencies import LoggedInUser, Admin, Staff
from dtos.auth import AccountResponse, UserRegisterResponse
from dtos.user import UsersResponse, UpdateRole, UpdateUserPassword

from services.user_service import UserService

router = APIRouter(prefix='/api/v1/users', tags=['Users'])


@router.get('/users', status_code=status.HTTP_200_OK, response_model=UsersResponse)
async def get_users(service: UserService, account: Staff):
    users = service.get_users()

    if users is None:
        raise HTTPException(status_code=404, detail='Users not found')

    return {'items': users}


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=AccountResponse)
async def get_user_by_id(user_id: int, service: UserService, account: Staff):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch('/update_role')
async def update_user_role(account: Admin, user_id: int, service: UserService, update: UpdateRole):
    updated_user = service.update_user_role(user_id, update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User role updated successfully"}


@router.patch('/update_password')
def register(user_id: int, req: UpdateUserPassword, account: Admin, service: UserService):
    updated_user = service.update_user_password(user_id, req)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User password updated successfully"}


@router.delete('/delete_user')
def delete(user_id: int, account: Admin, service: UserService):
    deleted_user = service.delete_user(user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User delete successfully"}

