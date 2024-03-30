import asyncio
import functools
import io
import logging

import discord
from discord.ext import commands
from PIL import Image, ImageDraw

_logger = logging.getLogger(__name__)


class Aim(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def generate_image(self, bytes: io.BytesIO) -> io.BytesIO:
        start_image = Image.open(fp=bytes)

        if start_image.mode != "RGB" or start_image.mode != "RGBA":
            start_image = start_image.convert("RGBA")

        middlex = start_image.width / 2
        middley = start_image.width / 2
        height = start_image.height
        width = start_image.width

        red = (255, 0, 0)  # (r, g, b)

        line_width = width // 30  # 128//30 = 4
        circle_radius = int(line_width * 1.5)
        rect_offset = (circle_radius + line_width) * 2

        left_rect_bounds = [(0, middley - line_width), (middlex - rect_offset, middley + line_width)]
        top_rect_bounds = [(middlex - line_width, 0), (middlex + line_width, middley - rect_offset)]
        right_rect_bounds = [(middlex + rect_offset, middley - line_width), (width, middley + line_width)]
        bottom_rect_bounds = [(middlex - line_width, middley + rect_offset), (middlex + line_width, height)]
        circle_bounds = [
            (middlex - circle_radius, middley - circle_radius),
            (middlex + circle_radius, middley + circle_radius),
        ]

        draw_obj = ImageDraw.Draw(start_image)
        draw_obj.ellipse(circle_bounds, red)
        draw_obj.rectangle(left_rect_bounds, red)  # type: ignore # idc
        draw_obj.rectangle(top_rect_bounds, red)  # type: ignore # idc
        draw_obj.rectangle(right_rect_bounds, red)  # type: ignore # idc
        draw_obj.rectangle(bottom_rect_bounds, red)  # type: ignore # idc

        buffered_image = io.BytesIO()
        start_image.save(buffered_image, "PNG")
        buffered_image.seek(0)

        return buffered_image

    async def get_user_pfp_bytes(self, user: discord.User) -> io.BytesIO:
        user = await self.bot.fetch_user(user.id)
        av_bytesIO = io.BytesIO(await user.display_avatar.read())  # Read into buffer
        av_bytesIO.seek(0)  # return to beginning.
        return av_bytesIO

    @commands.hybrid_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, attach_files=True)
    async def aim(self, ctx: commands.Context, user: discord.User) -> None:
        """Aim at someone.

        Parameters
        -----------
        user: discord.User
            Who should I aim at?
        """
        async with ctx.typing():
            _logger.debug(f"Processing aim for {user.id=} requested by {ctx.author.id=}")

            pfp_bytes = await self.get_user_pfp_bytes(user)
            to_run = functools.partial(self.generate_image, pfp_bytes)
            image = await asyncio.to_thread(to_run)
            await ctx.send(file=discord.File(image, "snipe.png"))


async def setup(bot):
    _logger.info("Loading cog Aim")
    await bot.add_cog(Aim(bot))


async def teardown(bot):
    _logger.info("Unloading cog Aim")
