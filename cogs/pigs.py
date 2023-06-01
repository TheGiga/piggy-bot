import datetime
import logging
import random
from typing import Any

import discord
from discord.ext.commands import cooldown, BucketType
from tortoise.exceptions import IntegrityError
from tortoise.queryset import QuerySet

import config
from src import Piggy, User, Pig, DefaultEmbed

words = {
    "weight": {
        "ru": "Вес",
        "uk": "Вага",
        "en_US": "Weight"
    },

    "age": {
        "ru": "Возраст",
        "uk": "Вік",
        "en_US": "Age"
    },

    "days": {
        "ru": "дн.",
        "uk": "дн.",
        "en_US": "d."
    },

    "name": {
        "ru": "Имя",
        "uk": "Ім'я",
        "en_US": "Name"
    }
}

def trw(word, locale, default='en_US'):
    x = words[word].get(locale)

    return x if x else words[word].get(default)

def tr(responses, locale, default = "en_US"):
    x = responses.get(locale)
    return x if x else responses.get(default)

class Pigs(discord.Cog):
    def __init__(self, bot):
        self.bot: Piggy = bot

    @discord.slash_command(
        name='pig',
        description='🐷 Information about specific pig',
        description_localizations={
            "ru": "🐷 Информация о хряке",
            "uk": "🐷 Інформація про хряка"
        }
    )
    @cooldown(1, 5, BucketType.user)
    async def pig(
            self, ctx: discord.ApplicationContext, name: discord.Option(
                str, description="name (case sensitive) | имя (уч. регистр)", required=False
            ) = None
    ):
        author, _ = await User.get_or_create(discord_id=ctx.user.id)

        locale = ctx.interaction.locale

        not_found = {
            "ru": "😢 Хряк с таким именем - не найден.",
            "uk": "😢 Хряк з таким іменем - не знайдений.",
            "en_US": "😢 Pig with such name is not found."
        }

        if name is None:
            pig = await author.get_pig()
        else:
            pig = await Pig.get_by_name(name)

            if pig is None:
                return await ctx.respond(tr(not_found, locale), ephemeral=True)

        embed = await pig.get_embed(ctx.interaction.locale)

        await ctx.respond(embed=embed)

    @discord.slash_command(
        name='feed',
        description='🐷 Feed your pig',
        description_localizations={
            "ru": "🐷 Покормить своего хряка",
            "uk": "🐷 Покормити свого хряка"
        }
    )
    @cooldown(1, 10800, BucketType.user)
    async def feed(self, ctx: discord.ApplicationContext):
        try:
            await ctx.defer()
        except discord.NotFound:
            print(f'Cannot defer in /feed, like always... (by {ctx.user}, at: {datetime.datetime.utcnow()} UTC)')
            pass

        locale = ctx.interaction.locale

        responses = {
            "-": {
                "ru": 'Ваш хряк похудел на **{} кг** 😢',
                "uk": 'Ваш хряк скинув салової маси на **{} кг** 😢',
                "en_US": 'Your pig lost **{} kg** in weight 😢'
            },
            "+": {
                "ru": 'Ваш хряк пожирнел на **{} кг** 😎',
                "uk": 'Ваш хряк нагнав салової маси на **{} кг** 😎',
                "en_US": 'Your pig gained **{} kg** in weight 😎'
            },
            "=": {
                "ru": 'Масса вашего хряка не изменилась... 🐷',
                "uk": 'Маса вашого хряка не змінилася... 🐷',
                "en_US": "Weight of your pig didn't change... 🐷"
            },
        }

        user, _ = await User.get_or_create(discord_id=ctx.user.id)
        pig = await user.get_pig()

        if 0 <= pig.weight <= 50:
            fat = random.randint(0, 30)
        else:
            fat = random.randint(-20, 30)

        old_weight = pig.weight

        await pig.add_weight(fat)

        if pig.weight < 0:
            pig.weight = 0
            await pig.save()

            fat = -old_weight

        embed = DefaultEmbed()
        embed.title = pig.name

        embed.add_field(name=f"🐷 {trw('weight', locale)}", value=f'{pig.weight} kg.')
        embed.add_field(name=f"🕐 {trw('age', locale)}", value=f"{pig.age.days} {trw('days', locale)}")
        embed.set_thumbnail(url='https://i.imgur.com/N45Jkdo.png')

        if fat < 0:
            embed.description = tr(responses["-"], locale).format(abs(fat))
        elif fat > 0:
            embed.description = tr(responses["+"], locale).format(fat)
        else:
            embed.description = tr(responses["="], locale)

        try:
            await ctx.respond(embed=embed)
        except discord.NotFound:
            await ctx.send(content=f"{ctx.user.mention}", embed=embed)

    @discord.slash_command(
        name='name',
        description="🐷 Change Pig's name",
        description_localizations={
            "ru": "🐷 Изменить имя своего хряка",
            "uk": "🐷 Змінити ім'я свого хряка"
        }
    )
    @cooldown(1, 30, BucketType.user)
    async def name(self, ctx: discord.ApplicationContext, name: discord.Option(str, "PIG'S NAME", max_length=20)):
        locale = ctx.interaction.locale

        responses = {
            "same_name": {
                "ru": "🤨 Вы уже дали такое-же имя своему хряку.",
                "uk": "🤨 Ви вже дали таке саме ім'я свому хряку.",
                "en_US": "🤨 You've already set the same name for your pig."
            },
            "already_exists": {
                "ru": "Имя `{}` уже занято 😢",
                "uk": "Ім'я `{}` вже зайняте 😢",
                "en_US": "The name `{}` is already taken 😢"
            },
            "created": {
                "ru": "✅ Вы успешно создали хряка с именем `{}`",
                "uk": "✅ Ви успішно створили хряка з іменем `{}`",
                "en_US": "✅ You have successfully created a pig with name `{}`"
            },
            "changed": {
                "ru": "☑️ Вы успешно сменили имя своего хряка с `{old}` на `{new}`.",
                "uk": "☑️ Ви успішно змінили ім'я свого хряка з `{old}` на `{new}`.",
                "en_US": "☑️ You have successfully changed your pig's name from `{old}` to `{new}`."
            }
        }

        user, created = await User.get_or_create(discord_id=ctx.user.id)
        pig = await user.get_pig()
        old_name = pig.name

        if pig.name == name:
            return await ctx.respond(tr(responses["same_name"], locale), ephemeral=True)

        try:
            await pig.set_name(name)
        except IntegrityError:
            return await ctx.respond(tr(responses["already_exists"], locale).format(name), ephemeral=True)

        if created:
            return await ctx.respond(tr(responses["created"], locale).format(name), ephemeral=True)

        try:
            await ctx.respond(
                tr(responses["changed"], locale).format(old=old_name, new=name),
                ephemeral=True
            )
        except discord.NotFound:
            await ctx.send(
                tr(responses["changed"], locale).format(old=old_name, new=name)
            )


    @cooldown(1, 5, BucketType.user)
    @discord.slash_command(
        name='top',
        description='🐷 Top 10 pigs by weight',
        description_localizations={
            "ru": "🐷 Топ хряков по жировой массе",
            "uk": "🐷 Топ 10 хряків за саловим запасом"
        }
    )
    async def top(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        query_set: list[Pig, Any] = await QuerySet(Pig).order_by('-weight').limit(10)

        leaderboard_content = ""

        for i, pig in enumerate(query_set, 1):
            discord_user = await pig.get_owner()
            leaderboard_content += f"{i}. {pig.name} - {pig.weight} kg.\n- # {discord_user}\n"

        leaderboard = f"```glsl\n{leaderboard_content}```"

        embed = DefaultEmbed()
        embed.title = "🐷 TOP 10"
        embed.description = leaderboard

        await ctx.respond(embed=embed)

    @cooldown(1, 60, BucketType.user)
    @discord.slash_command(
        name='report',
        description='🐖 Report user',
        description_localizations={
            "ru": "🐖 Жалоба на владельца хряка",
            "uk": "🐖 Скарга на користувача"
        }
    )
    async def report(
            self, ctx: discord.ApplicationContext,
            name: discord.Option(str, description="Имя хряка (уч. регистр)", max_length=30),
            reason: discord.Option(str, choices=config.REPORT_REASONS)
    ):
        await ctx.defer(ephemeral=True)

        locale = ctx.interaction.locale

        responses = {
            "not_found": {
                "ru": "😢 Хряк с таким именем - не найден.",
                "uk": "😢 Хряк з таким іменем - не знайдений.",
                "en_US": "😢 Pig with such name is not found."
            },

            "success": {
                "ru": "☑️ Репорт успешно отправлен, спасибо!",
                "uk": "☑️ Репорт успішно відправлено, дякуємо!",
                "en_US": "☑️ Thanks for the report!"
            }
        }

        pig = await Pig.get_by_name(name)

        if pig is None:
            return await ctx.respond(tr(responses["not_found"], locale), ephemeral=True)

        await ctx.defer(ephemeral=True)

        pig_owner = await pig.get_owner()

        await self.bot.send_critical_log(
            f'Репорт от пользователя `{ctx.user}` на хряка `{pig.name}`, хозяин: `{pig_owner} ({pig_owner.id})`'
            f'\n- Причина: `{reason}` ||<@352062534469156864>||', logging.CRITICAL
        )

        await ctx.respond(tr(responses["success"], locale), ephemeral=True)


def setup(bot):
    bot.add_cog(Pigs(bot))
