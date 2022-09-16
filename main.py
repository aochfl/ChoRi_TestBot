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
    # cog 하나씩 불러오기
    # activate_list = ["ping"]
    # for name in activate_list:
    #     await app.load_extension(f"Cogs.{name}")


@app.command(name="reload")
async def reload_extension(ctx, extension=None):
    if extension is not None:
        await unload_function(extension)
        try:
            await app.load_extension(f"Cogs.{extension}")
        except commands.ExtensionNotFound:
            await ctx.send(f":x: '{extension}'을(를) 파일을 찾을 수 없습니다!")
        except (commands.NoEntryPointError, commands.ExtensionFailed):
            await ctx.send(f":x: '{extension}'을(를) 불러오는 도중 에러가 발생했습니다!")
        else:
            await ctx.send(f":white_check_mark: '{extension}'을(를) 다시 불러왔습니다!")
    else:
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                await unload_function(filename[:-3])
                try:
                    await app.load_extension(f"Cogs.{filename[:-3]}")
                except commands.ExtensionNotFound:
                    await ctx.send(f":x: '{filename[:-3]}'을(를) 파일을 찾을 수 없습니다!")
                except (commands.NoEntryPointError, commands.ExtensionFailed):
                    await ctx.send(f":x: '{filename[:-3]}'을(를) 불러오는 도중 에러가 발생했습니다!")
        await ctx.send(":white_check_mark: reload 작업을 완료하였습니다!")


@app.command(name="unload")
async def unload_extension(ctx, extension=None):
    if extension is not None:
        await unload_function(extension)
        await ctx.send(f":white_check_mark: {extension}기능을 종료했습니다!")
    else:
        await unload_function(None)
        await ctx.send(":white_check_mark: 모든 확장기능을 종료했습니다!")


async def unload_function(extension=None):
    if extension is not None:
        try:
            await app.unload_extension(f"Cogs.{extension}")
        except (commands.ExtensionNotLoaded, commands.ExtensionNotFound):
            pass
    else:
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                try:
                    await app.unload_extension(f"Cogs.{filename[:-3]}")
                except (commands.ExtensionNotLoaded, commands.ExtensionNotFound):
                    pass


@app.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="몰?루", description="입력하신 명령어는 존재하지 않는 명령어입니다", color=0xFF0000)
        await ctx.reply(embed=embed)
        return
    else:
        embed = discord.Embed(title="오류!!", description="예상치 못한 오류가 발생했습니다.", color=0xFF0000)
        embed.add_field(name="상세", value=f"```{error}```")
        await ctx.reply(embed=embed)
        return


async def main():
    async with app:
        await load_extensions()
        file = open("discord_token.txt")
        bot_token = file.readline()
        file.close()
        await app.start(bot_token)


asyncio.run(main())