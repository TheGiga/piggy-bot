import discord
from discord.ext import tasks
from tortoise.exceptions import IntegrityError

import config
from src import Pig, Piggy


class Admin(discord.Cog):
    def __init__(self, bot):
        self.bot: Piggy = bot
        self.activity_updater.start()

    def cog_check(self, ctx: discord.ApplicationContext):
        return ctx.author.id in config.ADMINS

    admin = discord.SlashCommandGroup(name='admin', description='Административные команды')
    set = admin.create_subgroup(name='set')

    @set.command(name='name', description='Изменить имя любого хряка')
    async def set_name(
            self, ctx: discord.ApplicationContext,
            name: discord.Option(str, description="Имя хряка (уч. регистр)", max_length=30),
            new_name: discord.Option(str, description='Новое имя', max_length=20)
    ):
        pig = await Pig.get_by_name(name)

        if pig is None:
            return await ctx.respond('😢 Хряк с таким именем - не найден.', ephemeral=True)

        old_name = pig.name
        try:
            await pig.set_name(new_name)
        except IntegrityError:
            return await ctx.respond(f'Имя {new_name} уже занято 😢', ephemeral=True)

        await ctx.respond(f'Имя хряка `ID: {pig.id}` успешно изменено с `{old_name}` на `{pig.name}`.', ephemeral=True)

    @tasks.loop(minutes=10)
    async def activity_updater(self):
        await self.bot.wait_until_ready()
        await self.bot.change_presence(activity=discord.Game(name=f'{self.bot.member_count} users'))


def setup(bot):
    bot.add_cog(Admin(bot))
