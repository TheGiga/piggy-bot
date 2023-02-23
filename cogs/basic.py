import discord
from discord.ext.commands import cooldown, BucketType

from src import Piggy, DefaultEmbed, User


class Basic(discord.Cog):
    def __init__(self, bot):
        self.bot: Piggy = bot

    @discord.slash_command(name='help', description='Помощь по боту.')
    async def help_command(self, ctx: discord.ApplicationContext):
        await ctx.respond(embeds=self.bot.help_command())

    @cooldown(1, 5, BucketType.user)
    @discord.slash_command(name='user', description='👤 Информация о пользователе')
    async def user(
            self, ctx: discord.ApplicationContext, user: discord.Option(
                discord.Member, description='пользователь'
            ) = None
    ):
        if user is None:
            user = ctx.user

        local_user, _ = await User.get_or_create(discord_id=user.id)
        pig = await local_user.get_pig()

        embed = DefaultEmbed()
        embed.title = str(user)

        embed.add_field(name='🐷 Имя хряка', value=f'`{pig.name}`', inline=False)
        embed.add_field(name='🔢 UID', value=f'`{local_user.id}`', inline=False)

        embed.set_thumbnail(url=user.display_avatar)

        async def callback(interaction: discord.Interaction):
            await interaction.response.send_message(embed=await pig.get_embed(), ephemeral=True)

        view = discord.ui.View()
        button = discord.ui.Button(label='ㅤㅤИнформация о хрякеㅤㅤ', emoji='🐷')
        button.callback = callback
        view.add_item(button)

        await ctx.respond(embed=embed, view=view)


def setup(bot):
    bot.add_cog(Basic(bot))
