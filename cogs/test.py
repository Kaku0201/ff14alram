print(f"[LOAD] test.py ({__file__})")

from discord.ext import commands
from discord import app_commands, Interaction
from scheduler_module import get_subscription_state, generate_subscription_embed

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="알림테스트",
        description="자동 알림 메시지를 즉시 테스트합니다 (관리자 전용)."
    )
    @app_commands.choices(
        종류=[
            app_commands.Choice(name="전장", value="전장"),
            app_commands.Choice(name="청약", value="청약"),
        ]
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def 알림테스트(self, interaction: Interaction, 종류: app_commands.Choice[str]):
        if 종류.value == "전장":
            # 기존대로
            from scheduler_module import send_battleground_alert
            await send_battleground_alert(self.bot, [interaction.guild])
            await interaction.response.send_message("⚔️ 전장 알림 테스트 완료!", ephemeral=True)
            return

        # 청약 테스트: 지금 주기 상태 기준 자동
        state, start, end = get_subscription_state()
        now = interaction.created_at  # or use datetime.now(KST)
        기간_str = f"{start.strftime('%m월 %d일')} ~ {end.strftime('%m월 %d일')}"
        마감시간 = end.strftime('%m월 %d일 %H:%M')
        embed = None

        if state == "청약 신청 기간":
            # 만약 오늘이 마감일이고 시간도 23:50 이후면 마감 임베드!
            if now.date() == end.date() and now.hour == 23 and now.minute >= 50:
                embed = generate_subscription_embed("신청 마감", 기간_str, 마감시간)
            else:
                embed = generate_subscription_embed("신청 시작", 기간_str)
        elif state == "당첨 확인 기간":
            # 만약 오늘이 당첨확인 마감일이고 시간도 23:50 이후면 마감 임베드!
            if now.date() == end.date() and now.hour == 23 and now.minute >= 50:
                embed = generate_subscription_embed("당첨 마감", 기간_str, 마감시간)
            else:
                embed = generate_subscription_embed("당첨 확인 시작", 기간_str)
        else:
            embed = generate_subscription_embed("알 수 없는 상태", "지원되지 않는 상태입니다.")

        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("📅 청약 알림 테스트 완료!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Test(bot))
