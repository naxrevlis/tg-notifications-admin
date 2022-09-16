from tortoise import fields, models
from datetime import datetime


class Users(models.Model):
    id: int = fields.IntField(pk=True)
    username: str = fields.CharField(max_length=30, unique=True)
    first_name: str = fields.CharField(max_length=30, null=True)
    last_name: str = fields.CharField(max_length=30, null=True)
    password: str = fields.CharField(max_length=120)
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    modified_at: datetime = fields.DatetimeField(auto_now=True)


class Tokens(models.Model):
    id: int = fields.IntField(pk=True)
    token: str = fields.CharField(max_length=30, unique=False)
    user: fields.ForeignKeyRelation[Users] = fields.ForeignKeyField(
        "models.Users", related_name="tokens"
    )
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    modified_at: datetime = fields.DatetimeField(auto_now=True)

