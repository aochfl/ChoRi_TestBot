import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.all()
app = commands.Bot(command_prefix='!', intents=intents)


async def main():
    async with app:
        file = open("discord_token.txt")
        bot_token = file.readline()
        file.close()
        await app.start(bot_token)


@app.command()
async def ping(ctx):
    await ctx.send('pong')


@app.command(name="핑")
async def ping(ctx):
    await ctx.send('퐁')

asyncio.run(main())