from scheduler_module import start_schedulers
import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from keep_alive import keep_alive

# ✅ 디스코드 봇 설정
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ 슬래시 명령어 에러 처리 핸들러
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message(
            "❗이 명령어는 **관리자만 사용할 수 있어요!**", ephemeral=True)

# ✅ 봇 준비 완료 시
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    try:
        # 전 서버에 명령어 동기화
        await bot.tree.sync()  # 전역 등록 (모든 서버 대상)
        print(f"✅ Synced slash commands globally.")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")

# ✅ 확장(cogs) 로딩
async def load_extensions():
    await bot.load_extension("cogs.battleground")
    await bot.load_extension("cogs.subscription")
    await bot.load_extension("cogs.settings")
    await bot.load_extension("cogs.test")

# ✅ 메인 실행 함수
async def main():
    keep_alive()  # Flask 서버 실행 (UptimeRobot용)
    await load_extensions()
    await bot.start(os.environ['TOKEN'])

# ✅ 시작
if __name__ == "__main__":
    asyncio.run(main())
