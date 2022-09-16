from fastapi import APIRouter, status
from tortoise.contrib.fastapi import HTTPNotFoundError
import tg_notifications_admin.crud.users as users_crud

from tg_notifications_admin.schemas.users import UserInSchema, UserOutSchema

router = APIRouter()

@router.post("/register", response_model=UserOutSchema)
async def create_user(user: UserInSchema) -> UserOutSchema:
    return await users_crud.create_user(user)


@router.delete("/delete/{user_id}", response_model=UserOutSchema, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: int) -> UserOutSchema:
    return await users_crud.delete_user(user_id)