import datetime
from typing import Any

import discord
from tortoise import fields
from tortoise.models import Model

from src import bot_instance
from ..embed import DefaultEmbed


class Pig(Model):
    # Basic

    id = fields.IntField(pk=True)
    owner_id = fields.IntField(unique=True)

    weight = fields.IntField(default=0)
    name = fields.CharField(unique=True, max_length=32)
    creation_date = fields.DatetimeField()

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.creation_date = datetime.datetime.utcnow()
        self.name = f'{self.creation_date.strftime("%Y-%m-%d %H:%M:%S %f")}'

    def __int__(self):
        return self.id

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Pig({self.owner_id=}, {self.id=})'

    async def add_weight(self, x: int) -> None:
        self.weight += x
        await self.save()

    async def set_name(self, x: str) -> None:
        self.name = x
        await self.save()

    async def get_owner(self) -> discord.User:
        return await bot_instance.get_or_fetch_user(self.owner_id)

    async def get_embed(self, locale = "en_US") -> discord.Embed:
        from cogs.pigs import trw

        embed = DefaultEmbed()

        embed.title = self.name
        embed.description = f'OWNER: *`{(await self.get_owner()).name}`*'

        embed.set_thumbnail(url='https://i.imgur.com/EnJ65WL.png')
        embed.add_field(name=f"🐷 {trw('weight', locale)}", value=f'{self.weight} kg.')
        embed.add_field(name=f"🕐 {trw('age', locale)}", value=f"{self.age.days} {trw('days', locale)}")

        return embed

    @classmethod
    async def get_by_name(cls, name: str):
        return await cls.get_or_none(name=name)

    @property
    def age(self) -> datetime.timedelta:
        return datetime.datetime.utcnow() - self.creation_date.replace(tzinfo=None)
