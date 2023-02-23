from .pig import Pig
from tortoise import fields
from tortoise.models import Model


class User(Model):
    # Basic

    id = fields.IntField(pk=True)
    discord_id = fields.IntField()
    pig_id = fields.IntField(default=0)

    def __int__(self):
        return self.discord_id

    def __str__(self):
        return f"[ User with id {self.discord_id} ]"

    def __repr__(self):
        return f'User({self.discord_id=}, {self.id=})'

    async def get_pig(self) -> Pig:
        pig, _ = await Pig.get_or_create(owner_id=self.discord_id)

        return pig
