from fastapi import HTTPException, APIRouter
from starlette import status

from dependencies import LoggedInUser
from dtos.auth import AccountResponse, UserRegisterResponse
from dtos.user import UsersResponse, UpdateRole, UpdateUserPassword

from services.user_service import UserService

router = APIRouter(prefix='/api/v1/users', tags=['Users'])


@router.get('/users', status_code=status.HTTP_200_OK, response_model=UsersResponse)
async def get_users(service: UserService, account: LoggedInUser):

    users = service.get_users()

    if users is None:
        raise HTTPException(status_code=404, detail='Users not found')

    user_role = account.role.name
    if user_role == 'admin':
        return {'items': users}

    else:
        raise HTTPException(status_code=401, detail='Unauthorized')


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=AccountResponse)
async def get_user_by_id(user_id: int, service: UserService, account: LoggedInUser):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_role = account.role.name
    if user_role == 'admin':
        return user

    else:
        raise HTTPException(status_code=401, detail='Unauthorized')


@router.patch('/update_role')
async def update_user_role(user_id: int, service: UserService, account: LoggedInUser, update: UpdateRole):
    user_role = account.role.name

    if user_role == 'admin':
        updated_user = service.update_user_role(user_id, update)
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User role updated successfully"}
    else:
        raise HTTPException(status_code=401, detail='Unauthorized')


@router.patch('/update_password')
def register(user_id: int, req: UpdateUserPassword, account: LoggedInUser, service: UserService):
    user_role = account.role.name
    if user_role == 'admin':
        updated_user = service.update_user_password(user_id, req)
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User password updated successfully"}
    else:
        raise HTTPException(status_code=401, detail='Unauthorized')


@router.delete('/delete_user')
def delete(user_id: int, account: LoggedInUser, service: UserService):
    user_role = account.role.name
    if user_role == 'admin':
        deleted_user = service.delete_user(user_id)
        if deleted_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User delete successfully"}
    else:
        raise HTTPException(status_code=401, detail='Unauthorized')


''''''''''


@router.delete("/api/v1/users/{user_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user: user_dependency, db: db_dependency):
    return user_controllers.delete_user_controller(user_id, current_user, db)



def delete_user_controller(user_id: int, current_user: dict, db: Session):
    try:
        user_role = current_user.get('role')
        if user_role != "admin":
            raise HTTPException(status_code=403, detail='Access denied. User role not specified.')

        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        db.delete(user)
        db.commit()

        delete_refresh_token(user_id, db)

    except Exception as e:
        return {"Error": str(e)}
'''''''''

