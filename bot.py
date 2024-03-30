import datetime
import pkgutil

import cachetools
import discord
from discord.ext import commands


class SnipeBot(commands.AutoShardedBot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.STARTED_AT: datetime.datetime = discord.utils.utcnow()
        self.mem_cache: cachetools.TTLCache = cachetools.TTLCache(5000, 60.0)

    async def setup_hook(self):
        await self.load_extension("jishaku")

        extensions = [m.name for m in pkgutil.iter_modules(["extensions"], prefix="extensions.")]
        for extension in extensions:
            await self.load_extension(extension)

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.content != before.content:
            await self.process_commands(after)

    async def get_or_fetch_member(self, guild: discord.Guild, user_id: int, /) -> discord.Member | discord.User:
        """Gets or fetches a member/user given a guild and a user id.

        Members are cached using keys of (guild_id, user_id)

        Parameters
        ----------
        guild : discord.Guild
            The guild the Member is a part of
        user_id : int
            The id of the member to get

        Returns
        -------
        discord.Member | discord.User
            A member if cached or the Member has not left the Guild. Otherwise a User.
        """
        key = (guild.id, user_id)
        cached = self.mem_cache.get(key)

        if cached is not None:
            return cached

        try:
            member = await guild.fetch_member(user_id)
        except discord.NotFound:
            # Could error but should realistically not happen.
            # I see no real benefit to having this return None
            # or such to prevent the error so :shrugging:
            member = await self.fetch_user(user_id)

        self.mem_cache[key] = member

        return member
