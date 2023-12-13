import os
import asyncio
from dotenv import load_dotenv
from tortoise import connections

import config

load_dotenv()

from src import bot_instance, PiggyContext, db_init, User, Pig


async def main():
    await db_init()
    await bot_instance.start(os.getenv("TOKEN"))


@bot_instance.check
async def before_invoke_check(ctx: PiggyContext):
    # TODO: implement black list

    user, created = await User.get_or_create(discord_id=ctx.user.id)

    if not created:
        await user.update_last_interaction_time()
    else:
        pig = await Pig.get_or_none(owner_id=ctx.user.id, server_id=ctx.guild_id)

        if pig:
            await pig.set_activeness_status(True)

    return True


if __name__ == "__main__":

    for cog in config.COGS:
        bot_instance.load_extension(f'cogs.{cog}')
        print(f'☑ Loaded {cog}')

    event_loop = asyncio.get_event_loop_policy().get_event_loop()

    try:
        event_loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        print("🛑 Shutting Down")
        event_loop.run_until_complete(bot_instance.close())
        event_loop.run_until_complete(connections.close_all(discard=True))
        event_loop.stop()
