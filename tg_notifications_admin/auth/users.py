from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist

from tg_notifications_admin.database.models import Users
from tg_notifications_admin.schemas.users import UserDatabaseSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """Verify a plain password against a stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hash a password for storing."""
    return pwd_context.hash(password)


async def get_user(username: str) -> UserDatabaseSchema:
    """Get user by username."""
    try:
        return await UserDatabaseSchema.from_queryset_single(
            Users.get(username=username)
        )
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))


async def validate_user(user: OAuth2PasswordRequestForm = Depends()):
    """Validate user."""
    try:
        db_user = await get_user(user.username)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return db_user
