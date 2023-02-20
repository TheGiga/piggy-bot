import datetime
import random
from typing import Any, Union

import discord
from tortoise import fields
from tortoise.models import Model
from tortoise.queryset import QuerySetSingle

from src import bot_instance


class Pig(Model):
    # Basic

    id = fields.IntField(pk=True)
    owner_id = fields.IntField(unique=True)

    weight = fields.IntField(default=0)
    name = fields.CharField(unique=True, max_length=30)
    creation_date = fields.DatetimeField()

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.creation_date = datetime.datetime.utcnow()
        self.name = f'Безымянный хряк №{random.randint(100000, 999999)}'

    def __int__(self):
        return self.id

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Pig({self.owner_id=}, {self.id=})'

    @property
    def age(self) -> datetime.timedelta:
        return datetime.datetime.utcnow() - self.creation_date.replace(tzinfo=None)

    async def add_weight(self, x: int) -> None:
        self.weight += x
        await self.save()

    async def set_name(self, x: str) -> None:
        self.name = x
        await self.save()

    async def get_owner(self) -> discord.User:
        return await bot_instance.fetch_user(self.owner_id)

    @classmethod
    async def get_by_name(cls, name: str):
        return await cls.get_or_none(name=name)
