import datetime
from .pig import Pig
from tortoise import fields
from tortoise.models import Model


class User(Model):
    # Basic

    id = fields.IntField(pk=True)
    discord_id = fields.IntField()
    pigs_ids = fields.JSONField(default=[])
    last_interaction = fields.DatetimeField(auto_now_add=True)

    def __int__(self):
        return self.discord_id

    def __str__(self):
        return f"[ User with id {self.discord_id} ]"

    def __repr__(self):
        return f'User({self.discord_id=}, {self.id=})'

    async def get_pig(self, server_id: int) -> Pig:
        pig, created = await Pig.get_or_create(owner_id=self.discord_id, server_id=server_id)

        if created:
            self.pigs_ids.append(pig.id)
            await self.save()

        return pig

    async def get_all_pigs(self, only_active: bool = False) -> list[Pig]:
        pig_list = []

        for pig_id in self.pigs_ids:
            pig = await Pig.get_or_none(id=pig_id)

            if pig:
                if only_active:
                    pig_list.append(pig) if pig.active else None
                else:
                    pig_list.append(pig)

        return pig_list

    async def update_last_interaction_time(self, time: datetime.datetime = None):
        if not time:
            time = datetime.datetime.utcnow()

        self.last_interaction = time
        await self.save()
