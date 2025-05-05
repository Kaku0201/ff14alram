from scheduler_module import start_schedulers
import os
import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread
import asyncio

# --------------------------------------
# ✅ Flask 웹서버 (UptimeRobot용)
# --------------------------------------
app = Flask('')


@app.route('/')
def home():
    return "I'm alive!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


# --------------------------------------
# ✅ 디스코드 봇 설정
# --------------------------------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# --------------------------------------
# ✅ 봇 준비 완료 시 이벤트
# --------------------------------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")

    start_schedulers(bot)  # 스케줄러 시작


# --------------------------------------
# ✅ 확장(cogs) 로딩 함수
# --------------------------------------
async def load_extensions():
    await bot.load_extension("cogs.battleground")
    await bot.load_extension("cogs.subscription")
    await bot.load_extension("cogs.settings")  # 예: /채널설정 명령어용
    await bot.load_extension("cogs.test")


# --------------------------------------
# ✅ 메인 실행 함수
# --------------------------------------
async def main():
    keep_alive()
    await load_extensions()
    await bot.start(os.environ['TOKEN'])


# --------------------------------------
# ✅ 시작
# --------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
