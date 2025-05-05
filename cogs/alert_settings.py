import discord
from discord.ext import commands
from discord import app_commands
from utils import alert_utils


class AlertSettings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="알림설정", description="전장/청약 알림을 ON/OFF로 설정합니다.")
    @app_commands.describe(종류="설정할 알림 종류", 상태="알림을 켜거나 끌지 선택")
    @app_commands.choices(종류=[
        app_commands.Choice(name="전장", value="battleground"),
        app_commands.Choice(name="청약", value="subscription")
    ],
                          상태=[
                              app_commands.Choice(name="켜기", value="on"),
                              app_commands.Choice(name="끄기", value="off")
                          ])
    async def set_alert(self, interaction: discord.Interaction,
                        종류: app_commands.Choice[str],
                        상태: app_commands.Choice[str]):
        enabled = 상태.value == "on"
        alert_utils.set_alert(interaction.guild.id, 종류.value, enabled)

        msg = f"✅ `{종류.name}` 알림이 {'활성화' if enabled else '비활성화'}되었습니다."
        await interaction.response.send_message(msg, ephemeral=True)


async def setup(bot):
    await bot.add_cog(AlertSettings(bot))
