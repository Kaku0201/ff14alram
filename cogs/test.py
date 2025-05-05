from discord.ext import commands
from discord import app_commands, Interaction
from scheduler_module import send_battleground_alert, send_subscription_alert


class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="알림테스트",
                          description="자동 알림 메시지를 즉시 테스트합니다 (관리자 전용).")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(종류="battleground 또는 subscription")
    async def 알림테스트(self, interaction: Interaction, 종류: str):
        if 종류 not in ["battleground", "subscription"]:
            await interaction.response.send_message(
                "❌ 종류는 'battleground' 또는 'subscription' 중 하나만 가능합니다.",
                ephemeral=True)
            return

        if 종류 == "battleground":
            await send_battleground_alert(self.bot)
            await interaction.response.send_message("⚔️ 전장 알림 테스트 완료!",
                                                    ephemeral=True)
        else:
            await send_subscription_alert(self.bot)
            await interaction.response.send_message("📅 청약 알림 테스트 완료!",
                                                    ephemeral=True)


async def setup(bot):
    await bot.add_cog(Test(bot))
