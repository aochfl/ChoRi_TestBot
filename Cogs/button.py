import discord
from discord.ext import commands


class ButtonFunction(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=3)
        self.add_item(discord.ui.Button(label='Click Here', url="http://aochfl.tistory.com"))

    @discord.ui.button(label='primary', style=discord.ButtonStyle.primary, row=1)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("primary 누르셨습니다")

    @discord.ui.button(label='secondary', style=discord.ButtonStyle.secondary, row=1)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("secondary 누르셨습니다")

    @discord.ui.button(label='success', style=discord.ButtonStyle.success, row=2)
    async def button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("success 누르셨습니다")

    @discord.ui.button(label='danger', style=discord.ButtonStyle.danger, row=2)
    async def button4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("danger 누르셨습니다")


class Button(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.command(name='버튼')
    async def button(self, ctx):
        await ctx.send("버튼 명령어", view=ButtonFunction())


async def setup(app):
    await app.add_cog(Button(app))
