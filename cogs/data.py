import datetime
import logging

import discord
from discord.ext import tasks

import config
import loc
from discord.ext.commands import cooldown, BucketType
from src import Piggy, User, PiggyContext


class ConfirmDialog(discord.ui.View):
    def __init__(self, locale: loc):
        super().__init__()
        self.value = None
        self.disable_on_timeout = True
        self.timeout = 30.0
        self.locale = locale

    @discord.ui.button(label="YES", emoji="✅", style=discord.ButtonStyle.green)
    async def confirm_callback(
            self, button: discord.Button, interaction: discord.Interaction
    ):
        self.stop()
        self.disable_all_items()

        self.value = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="NO", emoji="❌", style=discord.ButtonStyle.grey)
    async def cancel_callback(
            self, button: discord.Button, interaction: discord.Interaction
    ):
        self.stop()
        self.disable_all_items()

        self.value = False

        await interaction.response.edit_message(view=self)


class Data(discord.Cog):
    def __init__(self, bot):
        self.bot: Piggy = bot
        self.inactive_users_purger.start()

    @discord.slash_command(
        name='delete_my_data', description=loc.en_US.DATA_DELETION_CMD_DESCRIPTION,
        description_localizations={
            "ru": loc.ru.DATA_DELETION_CMD_DESCRIPTION,
            "uk": loc.uk.DATA_DELETION_CMD_DESCRIPTION,
        }
    )
    @cooldown(1, 120, BucketType.user)
    async def data_deletion(self, ctx: PiggyContext):
        await ctx.defer(ephemeral=True)

        embed = discord.Embed(colour=discord.Colour.red(), title=ctx.translations.DATA_DELETION_EMBED_TITLE)
        embed.description = ctx.translations.DATA_DELETION_EMBED_DESCRIPTION

        view = ConfirmDialog(locale=ctx.translations)

        response = await ctx.respond(view=view, embed=embed)

        await view.wait()

        if view.value:
            local_user = await User.get_or_none(discord_id=ctx.user.id)

            if not local_user:
                return await response.edit(
                    embed=discord.Embed(
                        colour=discord.Colour.orange(),
                        description=ctx.translations.DATA_DELETION_NO_ASSOCIATED_DATA
                    )
                )

            pigs = await local_user.get_all_pigs()

            await local_user.delete()

            for pig in pigs:
                await pig.delete()

            await self.bot.send_critical_log(
                f"Deleted data for {local_user} due to request. Pigs: \n```{pigs}```", logging.INFO
            )

            await response.edit(
                embed=discord.Embed(
                    colour=discord.Colour.green(),
                    description=ctx.translations.DATA_DELETION_SUCCESS
                )
            )

    #@tasks.loop(seconds=15, reconnect=True)
    @tasks.loop(time=datetime.time(hour=3, tzinfo=datetime.timezone.utc), reconnect=True)
    async def inactive_users_purger(self):
        await self.bot.wait_until_ready()

        checklist = await User.all()

        for user in checklist:
            pigs = await user.get_all_pigs(only_active=True)

            for pig in pigs:
                pig_last_fed_x_ago = datetime.datetime.utcnow() - pig.last_fed.replace(tzinfo=None)

                if pig_last_fed_x_ago > datetime.timedelta(days=config.DATA_RETENTION_PERIOD_DAYS):
                    await pig.set_activeness_status(False)

            last_active_x_ago = datetime.datetime.utcnow() - user.last_interaction.replace(tzinfo=None)

            if last_active_x_ago > datetime.timedelta(days=config.DATA_RETENTION_PERIOD_DAYS):
                await user.delete()

                await self.bot.send_critical_log(
                    f"Deleted data for {user} due to inactivity. Pigs (retained for preservation):\n"
                    f"```{pigs}```", logging.INFO
                )

                print(
                    f"(!) Deleted records for user {user}, "
                    f"since they were last active {last_active_x_ago} ago..."
                )


def setup(bot):
    bot.add_cog(Data(bot))
