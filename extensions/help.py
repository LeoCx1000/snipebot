import logging

import discord
from discord.ext import commands

from bot import SnipeBot
from utils.color import randpastel_color

_logger = logging.getLogger(__name__)


SUPPORT_SERVER_URL = "https://discord.gg/f64pfnqbJJ"
SUPPORT_SERVER_HYPERLINK = f'[Support Server]({SUPPORT_SERVER_URL} "SnipeBot Support Server")'

BOT_HELP_DESCRIPTION = """
>>> Welcome to my help menu!

Use `~help command` for more help with a command.
Use `~help category` for more help with a category.

__**Available Commands**__
"""


def get_base_embed() -> discord.Embed:
    return discord.Embed(color=randpastel_color())


class HelpView(discord.ui.View):
    def __init__(self, mapping):
        super().__init__(timeout=180.0)


class SnipeBotHelp(commands.MinimalHelpCommand):
    context: commands.Context[SnipeBot]

    async def send_bot_help(self, mapping) -> None:
        embed = get_base_embed()
        embed.title = "SnipeBot"
        embed.description = BOT_HELP_DESCRIPTION

        for command in await self.filter_commands(self.context.bot.walk_commands()):
            if command:
                embed.description += f"{command.qualified_name}\n"

        embed.description = embed.description.strip()

        embed.add_field(
            name="Support Server",
            value=f"Please join the {SUPPORT_SERVER_HYPERLINK} if you need any help or would like to make a suggestion!",
        )

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog) -> None:
        embed = get_base_embed()
        embed.title = f"Cog: {cog.qualified_name}"
        embed.description = cog.description

        commands = await self.filter_commands(cog.get_commands())

        for command in commands:
            embed.add_field(name=command.name, value=command.short_doc, inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command: commands.Command) -> None:
        embed = get_base_embed()
        embed.title = f"Command: {command.qualified_name}"
        embed.description = f">>> {command.description}" if command.description else ""

        if len(command.clean_params.keys()) > 0:
            embed.description += "__**Options**__\n"
            for name, parameter in command.clean_params.items():
                embed.description += f"{name}: {parameter.description or 'No description provided.'}\n\n"

        embed.description = embed.description.strip()

        embed.add_field(name="Signature", value=f"{self.context.clean_prefix}{command.qualified_name} {command.signature}")
        embed.add_field(name="Aliases", value=", ".join(command.aliases) or "`None`")

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_group_help(self, group: commands.Group) -> None:
        subcommands = await self.filter_commands(group.commands)

        embed = get_base_embed()
        embed.title = f"Group: {group.qualified_name}"
        embed.description = group.description

        if len(subcommands) == 0:
            return await self.send_command_help(group)

        cmds_str = "\n".join(command.name for command in subcommands)

        embed.description += f">>> __**Subcommands**__\n{cmds_str}"

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error: str) -> None:
        embed = get_base_embed()
        embed.title = "Error"
        embed.description = error

        channel = self.get_destination()
        await channel.send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = SnipeBotHelp()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


async def setup(bot: commands.Bot):
    _logger.info("Loading cog Help")
    await bot.add_cog(Help(bot))


async def teardown(_: commands.Bot):
    _logger.info("Unloading cog Help")
