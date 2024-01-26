import calendar
import datetime

from loc import en_US, ru, uk
import logging
import os
from logging import WARNING, ERROR, CRITICAL

import aiohttp
import discord
from discord import CheckFailure, Webhook, Interaction
from discord.ext.commands import MissingPermissions, CommandOnCooldown

import config
from abc import ABC
from art import tprint

_intents = discord.Intents.default()


class PiggyContext(discord.ApplicationContext):
    def __init__(self, bot: 'Piggy', interaction: Interaction):
        super().__init__(bot, interaction)

    @property
    def translations(self):
        """
        :return: Interaction loc strings
        """
        locale = self.interaction.locale

        match locale:
            case "en_US":
                return en_US
            case "ru":
                return ru
            case "uk":
                return uk

            case _:
                return en_US


class Piggy(discord.Bot, ABC):
    def __init__(self, *args, **options):
        super().__init__(*args, **options)

        self.config = config

    async def get_application_context(
            self, interaction: discord.Interaction, cls=PiggyContext
    ):
        # The same method for custom application context.
        return await super().get_application_context(interaction, cls=cls)

    @property
    def member_count(self) -> int:
        count = 0

        for guild in self.guilds:
            count += guild.member_count

        return count

    def help_command(self) -> list[discord.Embed]:
        embed = discord.Embed()
        embed.colour = discord.Colour.embed_background()
        embed.title = "PIGBOT Commands"
        embed.set_image(url="https://i.imgur.com/WozcNGD.png")

        raw_commands = self.commands.copy()

        ordinary_commands = ''

        slash_count = 0
        for slash_count, slash in enumerate(
                [
                    command
                    for command in raw_commands
                    if type(command) is discord.SlashCommand
                ], 1
        ):
            ordinary_commands += f'{slash.mention} » {slash.description}\n'
            raw_commands.remove(slash)

        embed.description = f'**Slash Commands:** ({slash_count})\n{ordinary_commands}'

        group_embeds = []

        for group in [
            group
            for group in raw_commands
            if type(group) is discord.SlashCommandGroup and group.name not in config.EXCLUDED_HELP_CMD_GROUPS
        ]:
            group_embed = discord.Embed()
            group_embed.colour = discord.Colour.embed_background()
            group_embed.title = f'/{group.name}'
            group_embed.set_image(url="https://i.imgur.com/WozcNGD.png")

            group_commands = list(group.walk_commands())
            description = ''

            for subgroup in [
                sg
                for sg in group_commands
                if type(sg) is discord.SlashCommandGroup
            ]:
                value = ''

                for subgroup_command in subgroup.walk_commands():
                    value += f' - {subgroup_command.mention} » {subgroup_command.description}\n'
                    group_commands.remove(subgroup_command)

                group_embed.add_field(name=f"**/{subgroup.qualified_name}**:\n", value=value, inline=False)
                group_commands.remove(subgroup)

            # At this point, all non discord.SlashCommand entries should be removed
            print(group_commands)
            for group_command in group_commands:
                description += f"{group_command.mention} » {group_command.description}\n"

            group_embed.description = description

            group_embeds.append(group_embed)
            raw_commands.remove(group)

        return [embed, *group_embeds]

    async def on_application_command_error(
            self, ctx: discord.ApplicationContext, error: discord.ApplicationCommandError
    ):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(colour=discord.Colour.red(), title='👤 RESTRICTED!')
            embed.description = f"**❌ You are not allowed to use this command!**\n" \
                                f"❌ Вам запрещено использовать эту команду!"
            await ctx.respond(embed=embed, ephemeral=True)
            return

        elif isinstance(error, CommandOnCooldown):

            retry_at = datetime.datetime.utcnow() + \
                       datetime.timedelta(seconds=error.cooldown.get_retry_after())
            try:
                return await ctx.respond(
                    content=f'❌ This command is on cooldown, try again '
                            f'<t:{calendar.timegm(retry_at.timetuple())}:R>',
                    ephemeral=True
                )
            except discord.NotFound:
                await ctx.send(
                    f"{ctx.user.mention}, cooldown, try again "
                    f'<t:{calendar.timegm(retry_at.timetuple())}:R>'
                )

        elif isinstance(error, CheckFailure):
            embed = discord.Embed(colour=discord.Colour.red())
            embed.description = f"❌ Check failure!"
            await ctx.respond(embed=embed, ephemeral=True)
            return

        elif isinstance(error, discord.NotFound):
            print(f"❌ 'discord.NotFound' exception. Text:\n\n {error.text}")

        else:
            raise error

    @staticmethod
    async def send_critical_log(message: str, level: WARNING | ERROR | CRITICAL) -> None:
        """
        Message will be forwarded to local logging module + filesystem
        and also sent out via discord webhook if needed.

        :param level: level of log
        :param message: The message to be logged
        :return: None
        """

        logging.log(
            level=level,
            msg=message
        )

        content = f'`[{logging.getLevelName(level)}]` {message}'

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(os.getenv("LOGGING_WEBHOOK"), session=session)
            await webhook.send(content=content)

    async def on_ready(self):
        tprint("XPRKO6OT")
        print(f"✔ Bot is ready, logged in as {self.user}")


bot_instance = Piggy(intents=_intents)
