from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError
from passlib.context import CryptContext

from tg_notifications_admin.database.models import Users
from tg_notifications_admin.schemas.token import Status
from tg_notifications_admin.schemas.users import (
    UserInSchema,
    UserOutSchema,
    UserDatabaseSchema,
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user: UserInSchema) -> UserOutSchema:
    user.password = pwd_context.encrypt(user.password)
    try:
        user_obj = await Users.create(**user.dict(exclude_unset=True))
    except IntegrityError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return await UserOutSchema.from_tortoise_orm(user_obj)


async def delete_user(user_id: int, current_user: Users) -> Status:
    try:
        db_user = await UserOutSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))
    if db_user.id == current_user.id or current_user.is_admin:
        delete_count = await Users.filter(id=user_id).delete()
        if not delete_count:
            raise HTTPException(status_code=404, detail="User not found")
        return Status(message=f"User {user_id} deleted")
    raise HTTPException(
        status_code=401, detail="You are not allowed to delete this user"
    )


async def update_user(
    user_id: int, user_data: Users, current_user: Users
) -> UserOutSchema:
    try:
        db_user = await UserOutSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))
    if db_user.id == current_user.id or current_user.is_admin:
        update_count = await Users.filter(id=user_id).update(
            **user_data.dict(exclude_unset=True)
        )
        if not update_count:
            raise HTTPException(status_code=404, detail="User not found")
        return Status(message=f"User {user_id} updated")
    raise HTTPException(
        status_code=401, detail="You are not allowed to delete this user"
    )


async def get_users(current_user: Users) -> list[UserOutSchema]:
    if current_user.is_admin:
        return await UserOutSchema.from_queryset(Users.all())
    raise HTTPException(
        status_code=401, detail="You are not allowed to delete this user"
    )
