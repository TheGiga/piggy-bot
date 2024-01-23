import calendar
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
    owner_id = fields.IntField(unique=False)
    server_id = fields.IntField()

    weight = fields.IntField(default=0)
    name = fields.CharField(unique=True, max_length=32)
    creation_date = fields.DatetimeField()
    last_fed = fields.DatetimeField(auto_now_add=True)
    active = fields.BooleanField(default=True)

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.creation_date = datetime.datetime.utcnow()
        self.name = f'{self.creation_date.strftime("%Y-%m-%d %H:%M:%S %f")}'

    def __int__(self):
        return self.id

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Pig({self.owner_id=}, {self.id=}, {self.weight=}, {self.active=})'

    async def add_weight(self, x: int) -> None:
        self.weight += x
        await self.save()

    async def set_name(self, x: str) -> None:
        self.name = x
        await self.save()

    async def get_owner(self) -> discord.User:
        return await bot_instance.get_or_fetch_user(self.owner_id)

    async def set_last_feeding_time(self, time: datetime.datetime = None):
        if not time:
            time = datetime.datetime.utcnow()

        self.last_fed = time
        await self.save()

    async def set_activeness_status(self, status: bool):
        self.active = status
        await self.save()

    async def get_embed(self, translations) -> discord.Embed:
        embed = DefaultEmbed()

        status = translations.STATUS_ACTIVE if self.active else translations.STATUS_INACTIVE

        embed.title = self.name
        embed.description = f'OWNER: *`{(await self.get_owner()).name}`*'

        embed.set_thumbnail(url='https://i.imgur.com/EnJ65WL.png')
        embed.add_field(name=f"🐷 {translations.WEIGHT}", value=f'{self.weight} {translations.KG}')
        embed.add_field(name=f"🕐 {translations.AGE}", value=f"{self.age.days} {translations.DAYS}")
        embed.add_field(name=translations.STATUS, value=status)
        embed.add_field(name=translations.LAST_FED, value=f'<t:{calendar.timegm(self.last_fed.timetuple())}:R>')

        return embed

    @classmethod
    async def get_by_name(cls, name: str):
        return await cls.get_or_none(name=name)

    @property
    def age(self) -> datetime.timedelta:
        return datetime.datetime.utcnow() - self.creation_date.replace(tzinfo=None)
