from discord import app_commands
from discord.ext import commands
from utils.battleground_utils import format_battleground_embed


class Battleground(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="오늘의전장", description="오늘 포함 3일간의 전장 일정을 안내합니다.")
    async def 오늘의전장(self, interaction):
        embed = format_battleground_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Battleground(bot))
