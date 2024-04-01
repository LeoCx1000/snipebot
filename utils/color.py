import random

import discord


class PastelColor:
    def __new__(cls) -> discord.Color:
        return discord.Color.from_hsv(random.random(), 0.28, 0.97)
