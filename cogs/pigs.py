import datetime
import random
from typing import Any

import discord
from discord.ext.commands import cooldown, BucketType
from tortoise.queryset import QuerySet

from src import Piggy, User, Pig, DefaultEmbed


class Pigs(discord.Cog):
    def __init__(self, bot):
        self.bot: Piggy = bot

    @discord.slash_command(name='pig', description='🐷 Информация о хряке')
    @cooldown(1, 5, BucketType.user)
    async def pig(
            self, ctx: discord.ApplicationContext, name: discord.Option(
                str, description="имя хряка для просмотра профиля (уч. регистр)", required=False
            ) = None
    ):
        author, _ = await User.get_or_create(discord_id=ctx.user.id)

        embed = DefaultEmbed()

        if name is None:
            pig = await author.get_pig()
        else:
            pig = await Pig.get_by_name(name)

            if pig is None:
                return await ctx.respond('😢 Хряк с таким именем - не найден.', ephemeral=True)

        embed.title = pig.name
        embed.description = f'Хозяин хряка: *`{await pig.get_owner()}`*'

        embed.set_thumbnail(url='https://i.imgur.com/EnJ65WL.png')
        embed.add_field(name='🐷 Вес', value=f'{pig.weight} кг.')
        embed.add_field(name='⏲ Возраст', value=f'{pig.age.days} дней')

        await ctx.respond(embed=embed)

    @discord.slash_command(name='feed', description='🐷 Покормить своего хряка')
    @cooldown(1, 86400, BucketType.user)
    async def feed(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        user, _ = await User.get_or_create(discord_id=ctx.user.id)
        pig = await user.get_pig()

        fat = random.randint(3, 15)

        await pig.add_weight(fat)

        embed = DefaultEmbed()
        embed.title = pig.name
        embed.description = f'Ваш хряк пожирнел на **{fat} кг**!\n\n' \
                            f'{""}'

        embed.add_field(name='🐷 Вес', value=f'{pig.weight} кг.')
        embed.add_field(name='⏲ Возраст', value=f'{pig.age.days} дней')

        await ctx.respond(embed=embed)

    @discord.slash_command(name='name', description='🐷 Изменить имя своего хряка')
    @cooldown(1, 30, BucketType.user)
    async def name(self, ctx: discord.ApplicationContext, name: discord.Option(str, 'желаемое имя', max_length=20)):
        user, _ = await User.get_or_create(discord_id=ctx.user.id)
        pig = await user.get_pig()

        if pig.name == name:
            return await ctx.respond('🤨 Вы уже дали такое-же имя своему хряку.', ephemeral=True)

        await ctx.respond(f"☑ Вы успешно сменили имя своего хряка с `{pig.name}` на `{name}`", ephemeral=True)
        await pig.set_name(name)

    @cooldown(1, 5, BucketType.user)
    @discord.slash_command(name='top', description='🐷 Топ хряков по жировой массе')
    async def top(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        query_set: list[Pig, Any] = await QuerySet(Pig).order_by('-weight').limit(10)

        leaderboard = ""

        for i, pig in enumerate(query_set, 1):
            discord_user = await pig.get_owner()
            leaderboard += f"{i}. {pig.name} - `{pig.weight} кг` || {discord_user} ||\n"

        embed = DefaultEmbed()
        embed.title = "🐷 Топ 10 хряков"
        embed.description = leaderboard

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Pigs(bot))
