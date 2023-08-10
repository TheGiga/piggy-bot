import discord
import loc
from discord.ext.commands import cooldown, BucketType
from src import Piggy, DefaultEmbed, User, PiggyContext


class Basic(discord.Cog):
    def __init__(self, bot):
        self.bot: Piggy = bot

    @discord.slash_command(name='help', description='Help me please!')
    async def help_command(self, ctx: PiggyContext):
        await ctx.respond(embeds=self.bot.help_command())

    @cooldown(1, 5, BucketType.user)
    @discord.slash_command(
        name='user',
        description=loc.en_US.USER_CMD_DESCRIPTION,
        description_localizations={
            "ru": loc.ru.USER_CMD_DESCRIPTION,
            "uk": loc.uk.USER_CMD_DESCRIPTION,
        }
    )
    async def user(
            self, ctx: PiggyContext,
            user: discord.Option(
                discord.Member, description='пользователь / user'
            ) = None,
            uid: discord.Option(
                int, description='либо его UID / or his UID'
            ) = None
    ):
        if not user and not uid:
            user = ctx.user

        if uid and not user:
            print(uid)
            local_user = await User.get_or_none(id=uid)

            if not local_user:
                return await ctx.respond(f":x: UID `{uid}` not found!", ephemeral=True)

            user = await ctx.bot.get_or_fetch_user(local_user.discord_id)

            pig = await local_user.get_pig()
        else:
            local_user, _ = await User.get_or_create(discord_id=user.id)
            pig = await local_user.get_pig()

        embed = DefaultEmbed()
        embed.title = user.name

        embed.add_field(name=f'🐷 {ctx.translations.NAME}', value=f'`{pig.name}`', inline=False)
        embed.add_field(name=f'🔢 {ctx.translations.UID}', value=f'`{local_user.id}`', inline=False)

        embed.set_thumbnail(url=user.display_avatar.url)

        async def callback(interaction: discord.Interaction):
            await interaction.response.send_message(embed=await pig.get_embed(ctx.translations), ephemeral=True)

        view = discord.ui.View(disable_on_timeout=True, timeout=30.0)
        button = discord.ui.Button(label=f"{ctx.translations.PIG_PROFILE}", emoji='🐷')
        button.callback = callback
        view.add_item(button)

        await ctx.respond(embed=embed, view=view)


def setup(bot):
    bot.add_cog(Basic(bot))
