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

# ✅ config 객체를 bot에 저장
config = get_config()
bot.config = config
bot.save_config = save_config

# ✅ 봇 준비 완료 시
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")
    start_schedulers(bot)

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
