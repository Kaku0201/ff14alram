print(f"[LOAD] main.py ({__file__})")

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
        await bot.tree.sync()
        print(f"✅ Synced slash commands globally.")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")

# ✅ 코그(확장) 로딩 (오직 test만)
async def load_extensions():
    print("=== BEFORE test.py load ===")
    try:
        await bot.load_extension("cogs.test")
        print("=== test.py load SUCCESS ===")
    except Exception as e:
        print(f"=== test.py load ERROR: {e} ===")

# ✅ 메인 실행 함수
async def main():
    keep_alive()
    print("==== BEFORE LOAD EXTENSIONS ====")
    await load_extensions()
    print("==== AFTER LOAD EXTENSIONS ====")
    start_schedulers(bot)
    await bot.start(os.environ['TOKEN'])

if __name__ == "__main__":
    asyncio.run(main())
