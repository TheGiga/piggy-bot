import datetime

import discord
from discord.ext.commands import has_permissions

import config
from src import Piggy, PiggyContext, DefaultEmbed
from src.cooldown import PerGuildCooldownManager
from src.models import Guild


class Admin(discord.Cog):
    def __init__(self, bot):
        self.bot: Piggy = bot

    configuration = discord.SlashCommandGroup(name='config', description='Administrative commands and configuration')

    @has_permissions(administrator=True)
    @configuration.command(name='value')
    async def config_value(
            self, ctx: PiggyContext,
            key: discord.Option(str, choices=config.AVAILABLE_CONFIG_OPTIONS),
            value: discord.Option(str, required=False, default=None, description="leave empty to see the current value")
    ):
        if value is None:
            guild, _ = await Guild.get_or_create(discord_id=ctx.guild_id)
            value = guild.get_config_option(key)

            return await ctx.respond(f"`{key}`: `{value}`", ephemeral=True)

        cfg_options = config.AVAILABLE_CONFIG_OPTIONS
        check = cfg_options[key]["value_check_procedure"]

        if not check(value):
            return await ctx.respond(
                content=ctx.translations.GUILD_CONFIG_VALUE_ERROR.format(cfg_options[key]["value_check_requirements"]),
                ephemeral=True
            )

        guild, _ = await Guild.get_or_create(discord_id=ctx.guild_id)
        await guild.assert_config_option(key=key, value=value)

        if key == "cooldown":  # TODO: idk, come up with a better solution???
            cdm = PerGuildCooldownManager.register_or_get(guild=ctx.guild, time=datetime.timedelta(minutes=int(value)))
            cdm.change_time(time=datetime.timedelta(minutes=int(value)))

        await ctx.respond(ctx.translations.GUILD_CONFIG_VALUE_SUCCESS.format(key, value), ephemeral=True)

    @has_permissions(administrator=True)
    @configuration.command(name='help')
    async def config_help(self, ctx: PiggyContext):
        available_keys = ""
        cfg_options = config.AVAILABLE_CONFIG_OPTIONS

        for key in config.AVAILABLE_CONFIG_OPTIONS:
            available_keys += (
                f"* **`{key}`**\n"
                f"> {cfg_options[key]['comment']}\n"
                f"> Default: `{cfg_options[key]['default_value']}`"
            )

        embed = DefaultEmbed()
        embed.title = ctx.translations.GUILD_CONFIG_HELP_EMBED_TITLE
        embed.description = f'{available_keys}\n\n{ctx.translations.GUILD_CONFIG_HELP_INSTRUCTIONS}'

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))
