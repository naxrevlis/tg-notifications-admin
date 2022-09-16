from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError
from passlib.context import CryptContext

from tg_notifications_admin.database.models import Users
from tg_notifications_admin.schemas.users import UserInSchema, UserOutSchema, UserDatabaseSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user: UserInSchema) -> UserOutSchema:
    user.password = pwd_context.encrypt(user.password)
    try:
        user_obj = await Users.create(**user.dict(exclude_unset=True))
    except IntegrityError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return await UserOutSchema.from_tortoise_orm(user_obj)


async def delete_user(id: int) -> UserOutSchema:
    try:
        db_user = await UserOutSchema.from_queryset_single(Users.get(id=id))
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))
    user_obj = await Users.get(id=id)
    try:
        await user_obj.delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return await UserOutSchema.from_tortoise_orm(user_obj.id)