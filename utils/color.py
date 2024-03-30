import random

import discord


def randpastel_color() -> discord.Color:
    return discord.Color.from_hsv(random.random(), 0.28, 0.97)
