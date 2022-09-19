from datetime import timedelta


from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tortoise.contrib.fastapi import HTTPNotFoundError

import tg_notifications_admin.crud.users as users_crud
from tg_notifications_admin.auth.users import validate_user
from tg_notifications_admin.schemas.token import Status

from tg_notifications_admin.schemas.users import UserInSchema, UserOutSchema

from tg_notifications_admin.auth.jwthandler import (
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


router = APIRouter()


@router.post("/register", response_model=UserOutSchema)
async def create_user(user: UserInSchema) -> UserOutSchema:
    return await users_crud.create_user(user)


@router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    user = await validate_user(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token = jsonable_encoder(access_token)
    content = {"message": "You are logged in"}
    response = JSONResponse(content=content)
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=False,
    )
    return response


@router.delete(
    "/users/{user_id}/delete",
    response_model=UserOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_user(
    user_id: int, current_user: UserOutSchema = Depends(get_current_user)
) -> Status:
    """Delete a user."""
    return await users_crud.delete_user(user_id, current_user)


@router.put(
    "/users/{user_id}/update",
    response_model=UserOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def update_user(
    user_id: int, current_user: UserOutSchema = Depends(get_current_user)
) -> Status:
    """Update user"""
    return await users_crud.update_user(user_id, current_user)


@router.get("/users", response_model=list[UserOutSchema])
async def get_users() -> list[UserOutSchema]:
    """Get all users"""
    print(await users_crud.get_users())
    return await users_crud.get_users()
