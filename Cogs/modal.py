import discord
from discord.ext import commands


class Introduce(discord.ui.Modal, title='소개하기'):
    name = discord.ui.TextInput(
        label='닉네임',
        style=discord.TextStyle.short,
        placeholder='닉네임을 입력해주세요',
    )

    answer = discord.ui.TextInput(
        label='한줄소개',
        style=discord.TextStyle.long,
        placeholder='아무말이나 입력해주세요',
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'{self.name.value} 님이 추가되었습니다! \n{self.name.value} : {self.answer.value}')


class ModalButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=10)

    @discord.ui.button(label='모달생성', style=discord.ButtonStyle.primary)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Introduce())


class Modal(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.command(name='모달')
    async def select(self, ctx):
        await ctx.send(view=ModalButton())


async def setup(app):
    await app.add_cog(Modal(app))
