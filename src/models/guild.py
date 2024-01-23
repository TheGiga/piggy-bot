import config
from tortoise import fields
from tortoise.models import Model


class Guild(Model):
    # Basic

    id = fields.IntField(pk=True)
    discord_id = fields.IntField()
    config = fields.JSONField(default=config.DEFAULT_GUILD_CONFIG)

    def __int__(self):
        return self.discord_id

    def __str__(self):
        return f"[ Guild with id {self.discord_id} ]"

    def __repr__(self):
        return f'Guild({self.discord_id=}, {self.id=})'

    def get_config_option(self, key: str):
        return self.config.get(key)

    async def assert_config_option(self, key: str, value):
        self.config[key] = value
        await self.save()

    async def reset_config(self):
        self.config = config.DEFAULT_GUILD_CONFIG
        await self.save()
