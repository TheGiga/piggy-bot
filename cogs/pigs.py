import calendar
import datetime
import logging
import random
from typing import Any

import discord
from discord.ext.commands import cooldown, BucketType
from tortoise.exceptions import IntegrityError
from tortoise.queryset import QuerySet

import config
import loc
from src import Piggy, User, Pig, DefaultEmbed, PiggyContext


class Pigs(discord.Cog):
    def __init__(self, bot):
        self.bot: Piggy = bot

    @discord.slash_command(
        name='pig',
        description=loc.en_US.PIG_CMD_DESCRIPTION,
        description_localizations={
            "ru": loc.ru.PIG_CMD_DESCRIPTION,
            "uk": loc.uk.PIG_CMD_DESCRIPTION
        }
    )
    @cooldown(1, 5, BucketType.user)
    async def pig(
            self, ctx: PiggyContext, name: discord.Option(
                str, description="name (case sensitive) | имя (уч. регистр)", required=False
            ) = None
    ):
        author, created = await User.get_or_create(discord_id=ctx.user.id)

        if name is None:
            pig = await author.get_pig(ctx.guild_id)
        else:
            pig = await Pig.get_by_name(name)

            if pig is None:
                return await ctx.respond(ctx.translations.NAME_NOT_FOUND, ephemeral=True)

        status = ctx.translations.STATUS_ACTIVE if pig.active else ctx.translations.STATUS_INACTIVE

        embed = await pig.get_embed(ctx.translations)

        embed.add_field(name=ctx.translations.STATUS, value=status)
        embed.add_field(name=ctx.translations.LAST_FED, value=f'<t:{calendar.timegm(pig.last_fed.timetuple())}:R>')

        await ctx.respond(embed=embed, content=ctx.translations.CHANGE_NAME_PROPOSAL if created else "")

    @discord.slash_command(
        name='feed',
        description=loc.en_US.FEED_CMD_DESCRIPTION,
        description_localizations={
            "ru": loc.ru.FEED_CMD_DESCRIPTION,
            "uk": loc.uk.FEED_CMD_DESCRIPTION
        }
    )
    @cooldown(1, config.FEED_COMMAND_COOLDOWN_SECONDS, BucketType.member)
    async def feed(self, ctx: PiggyContext):
        try:
            await ctx.defer()
        except discord.NotFound:
            print(f'Cannot defer in /feed, like always... (by {ctx.user}, at: {datetime.datetime.utcnow()} UTC)')
            pass

        user, created = await User.get_or_create(discord_id=ctx.user.id)
        pig = await user.get_pig(ctx.guild_id)

        if 0 <= pig.weight <= 50:
            fat = random.randint(1, 30)
        else:
            fat = random.randint(-20, 30)

        old_weight = pig.weight

        await pig.add_weight(fat)

        if pig.weight < 0:
            pig.weight = 0
            await pig.save()

            fat = -old_weight

        await pig.set_last_feeding_time()
        if not pig.active:
            await pig.set_activeness_status(True)

        embed = DefaultEmbed()
        embed.title = pig.name

        embed.add_field(name=f"🐷 {ctx.translations.WEIGHT}", value=f'{pig.weight} {ctx.translations.KG}')
        embed.add_field(name=f"🕐 {ctx.translations.AGE}", value=f"{pig.age.days} {ctx.translations.DAYS}")
        embed.set_thumbnail(url='https://i.imgur.com/N45Jkdo.png')

        if fat < 0:
            embed.description = ctx.translations.WEIGHT_CHANGE_MINUS.format(abs(fat))
        elif fat > 0:
            embed.description = ctx.translations.WEIGHT_CHANGE_PLUS.format(fat)
        else:
            embed.description = ctx.translations.WEIGHT_CHANGE_SAME

        try:
            await ctx.respond(embed=embed, content=ctx.translations.CHANGE_NAME_PROPOSAL if created else "")
        except discord.NotFound:
            await ctx.send(content=f"{ctx.user.mention}", embed=embed)

    @discord.slash_command(
        name='name',
        description=loc.en_US.NAME_CMD_DESCRIPTION,
        description_localizations={
            "ru": loc.ru.NAME_CMD_DESCRIPTION,
            "uk": loc.uk.NAME_CMD_DESCRIPTION
        }
    )
    @cooldown(1, 30, BucketType.user)
    async def name(self, ctx: PiggyContext, name: discord.Option(str, "PIG'S NAME", max_length=20)):
        user, created = await User.get_or_create(discord_id=ctx.user.id)
        pig = await user.get_pig(ctx.guild_id)
        old_name = pig.name

        if pig.name == name:
            return await ctx.respond(ctx.translations.SAME_NAME, ephemeral=True)

        try:
            await pig.set_name(name)
        except IntegrityError:
            return await ctx.respond(ctx.translations.NAME_ALREADY_EXISTS.format(name), ephemeral=True)

        if created:
            return await ctx.respond(ctx.translations.PIG_CREATED.format(name), ephemeral=True)

        await ctx.respond(
            ctx.translations.NAME_CHANGED.format(old_name, name),
            ephemeral=True
        )

    @cooldown(1, 5, BucketType.user)
    @discord.slash_command(
        name='top',
        description=loc.en_US.TOP_CMD_DESCRIPTION,
        description_localizations={
            "ru": loc.ru.TOP_CMD_DESCRIPTION,
            "uk": loc.uk.TOP_CMD_DESCRIPTION
        }
    )
    async def top(self, ctx: PiggyContext, leaderboard_type: discord.Option(name="type", choices=['local', 'global'])):
        await ctx.defer()

        basic_query = QuerySet(Pig).order_by('-weight').filter(active=True).limit(10)

        if leaderboard_type == "local":
            query_set: list[Pig, Any] = await basic_query.filter(server_id=ctx.guild_id)
        else:
            query_set: list[Pig, Any] = await basic_query

        leaderboard_content = ""

        for i, pig in enumerate(query_set, 1):
            discord_user = await pig.get_owner()
            leaderboard_content += f"{i}. {pig.name} - {pig.weight} {ctx.translations.KG}.\n- # {discord_user.name}\n"

        leaderboard = f"```glsl\n{leaderboard_content if leaderboard_content else 'Empty...'}```"

        embed = DefaultEmbed()
        embed.title = f"{ctx.translations.TOP_10} | {leaderboard_type.upper()}"
        embed.description = leaderboard

        await ctx.respond(embed=embed)

    @cooldown(1, 60, BucketType.user)
    @discord.slash_command(
        name='report',
        description=loc.en_US.REPORT_CMD_DESCRIPTION,
        description_localizations={
            "ru": loc.ru.REPORT_CMD_DESCRIPTION,
            "uk": loc.uk.REPORT_CMD_DESCRIPTION
        }
    )
    async def report(
            self, ctx: PiggyContext,
            name: discord.Option(str, description="name of the pig (case sensitive)", max_length=30),
            reason: discord.Option(str, description="reason of the report (f.e: ToS violation)")
    ):
        await ctx.defer(ephemeral=True)

        pig = await Pig.get_by_name(name)

        if pig is None:
            return await ctx.respond(ctx.translations.NAME_NOT_FOUND, ephemeral=True)

        pig_owner = await pig.get_owner()

        await self.bot.send_critical_log(
            f'Report from `{ctx.user}` on pig `{pig.name}`, owner: `{pig_owner} ({pig_owner.id})`'
            f'\n- Reason: `{reason}` ||<@352062534469156864>||', logging.CRITICAL
        )

        await ctx.respond(ctx.translations.REPORT_SUCCESS, ephemeral=True)


def setup(bot):
    bot.add_cog(Pigs(bot))
