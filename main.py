import asyncio
import logging
import logging.handlers

import asyncpg
import discord

from bot import SnipeBot
from config import DB_URL, MAX_MESSAGES, PREFIX, TESTING, TOKEN

intents = discord.Intents(guilds=True, members=True, messages=True, reactions=True, message_content=True)
mem_cache_flags = discord.MemberCacheFlags.none()


# TODO
def logging_setup():
    if TESTING:
        discord.utils.setup_logging()

    else:
        log_fmt = logging.Formatter(
            fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        trfh = logging.handlers.TimedRotatingFileHandler("logs/snipebot.log", when="midnight", backupCount=15)
        trfh.setLevel(logging.DEBUG)
        trfh.setFormatter(log_fmt)


async def main():
    # TODO
    logging_setup()

    async with (
        asyncpg.create_pool(DB_URL) as pool,
        SnipeBot(
            command_prefix=PREFIX,
            pool=pool,
            intents=intents,
            member_cache_flags=mem_cache_flags,
            max_messages=MAX_MESSAGES,
        ) as bot,
    ):
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
