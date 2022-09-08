import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command(name="핑")
    async def ping2(self, ctx):
        embed = discord.Embed(title="ping pong", description="핑퐁", colour=0xffffff)
        embed.set_author(name='Author name', icon_url="https://han.gl/XBMeC")
        embed.set_footer(text="footer", icon_url="https://han.gl/XBMeC")
        embed.set_image(url="https://han.gl/XBMeC")
        embed.set_thumbnail(url="https://han.gl/XBMeC")
        embed.add_field(name="필드1", value="inline false 필드1 내용", inline=False)
        embed.add_field(name="필드2", value="inline false 필드2 내용", inline=False)
        embed.add_field(name="필드3", value="inline True 필드3 내용", inline=True)
        embed.add_field(name="필드4", value="inline True 필드4 내용", inline=True)
        await ctx.reply('퐁', embed=embed)


async def setup(app):
    await app.add_cog(Ping(app))



