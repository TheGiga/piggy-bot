import discord
from discord.ext import tasks
from tortoise.exceptions import IntegrityError

import config
from src import Pig, Piggy, PiggyContext


class Admin(discord.Cog):
    def __init__(self, bot):
        self.bot: Piggy = bot
        self.activity_updater.start()

    def cog_check(self, ctx: PiggyContext):
        return ctx.author.id in config.ADMINS

    admin = discord.SlashCommandGroup(name='admin', description='Административные команды')
    set = admin.create_subgroup(name='set')

    @set.command(name='name', description='Изменить имя любого хряка')
    async def set_name(
            self, ctx: PiggyContext,
            name: discord.Option(str, description="Имя хряка (уч. регистр)", max_length=32),
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

    @admin.command(name='announce', description='ANNOUNCE TO ALL SERVERS, should be used extremely rarely.')
    async def announce_message(self, ctx: PiggyContext, message: str):
        await ctx.defer()

        successes, errors = 0, 0

        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                try:
                    await channel.send(message)
                    successes += 1

                    break
                except discord.DiscordException:
                    errors += 1
                    continue

        await ctx.respond(f"{successes=}, {errors=}")

    @tasks.loop(minutes=10)
    async def activity_updater(self):
        await self.bot.wait_until_ready()
        await self.bot.change_presence(activity=discord.Game(name=f'{self.bot.member_count} users'))


def setup(bot):
    bot.add_cog(Admin(bot))
