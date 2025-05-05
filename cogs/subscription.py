from discord import app_commands
from discord.ext import commands
from utils.subscription_utils import get_subscription_state, generate_subscription_embed
from datetime import timedelta


class Subscription(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="오늘의청약", description="현재 청약 상태를 확인합니다.")
    async def 오늘의청약(self, interaction):
        state, start, end = get_subscription_state()
        now = start.tzinfo.localize(
            interaction.created_at
        ) if interaction.created_at.tzinfo is None else interaction.created_at

        기간_str = f"{start.strftime('%m월 %d일')} ~ {end.strftime('%m월 %d일')}"
        마감시간 = end.strftime('%m월 %d일 %H:%M')

        if state == "청약 신청 기간":
            embed = generate_subscription_embed("신청 시작", 기간_str)
        else:
            embed = generate_subscription_embed("당첨 확인 시작", 기간_str)

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Subscription(bot))
