import datetime

import discord

cooldown_managers: dict[int, 'PerGuildCooldownManager'] = {}


class PerGuildCooldownManager:
    def __init__(self, guild, time):
        self.time: datetime.timedelta = time
        self.guild: discord.Guild = guild

        # {user_id: cooldown_start_time}
        self.data: dict = {}

    def change_time(self, time: datetime.timedelta):
        self.time = time

    def add_user(self, user: discord.User):
        self.data[user.id] = datetime.datetime.utcnow()

    def retry_at(self, user: discord.User) -> datetime.datetime:
        cooldown_start_time = self.data.get(user.id)

        if not cooldown_start_time:
            return datetime.datetime.utcnow()

        cooldown_end_time = cooldown_start_time + self.time

        return cooldown_end_time

    def is_on_cooldown(self, user: discord.User) -> bool:
        cooldown_start_time = self.data.get(user.id)

        if not cooldown_start_time:
            return False

        cooldown_end_time = cooldown_start_time + self.time
        if cooldown_end_time < datetime.datetime.utcnow():
            self.data.pop(user.id)
            return False

        return True

    @classmethod
    def register_or_get(cls, guild: discord.Guild, time: datetime.timedelta) -> 'PerGuildCooldownManager':
        existing_record = cooldown_managers.get(guild.id)

        if not existing_record:
            existing_record = PerGuildCooldownManager(guild, time)
            cooldown_managers[guild.id] = existing_record

        return existing_record

    @classmethod
    def get_by_guild(cls, guild_id: int) -> 'PerGuildCooldownManager':
        return cooldown_managers.get(guild_id)
