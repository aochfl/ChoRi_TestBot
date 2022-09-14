import discord
from discord.ext import commands


class SelectFunction(discord.ui.Select):
    def __init__(self):
        options = []
        for index in range(0, 5):
            options.append(discord.SelectOption(label=f'label_{index}',
                                                description=f'description_{index}', value=f'value_{index}'))
        super().__init__(placeholder='Select 기능', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.channel.send(interaction.data["values"][0]+"을 선택하셨습니다.")
        await interaction.message.delete()


class SelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SelectFunction())


class Select(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.command(name='선택')
    async def select(self, ctx):
        await ctx.send("선택 명령어", view=SelectView())


async def setup(app):
    await app.add_cog(Select(app))
