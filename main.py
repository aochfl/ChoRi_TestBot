import asyncio
import os
import discord
from discord.ext import commands

intents = discord.Intents.all()
app = commands.Bot(command_prefix='!', intents=intents)


async def load_extensions():
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            await app.load_extension(f"Cogs.{filename[:-3]}")
        await load_extensions()
    # cog 하나씩 불러오기
    # activate_list = ["ping"]
    # for name in activate_list:
    #     await app.load_extension(f"Cogs.{name}")


async def main():
    async with app:
        await load_extensions()
        file = open("discord_token.txt")
        bot_token = file.readline()
        file.close()
        await app.start(bot_token)


asyncio.run(main())