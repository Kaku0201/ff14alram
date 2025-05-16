print(f"[LOAD] scheduler_module.py ({__file__})")

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.subscription_utils import get_subscription_state, generate_subscription_embed
from utils.battleground_utils import format_battleground_embed
import discord
import json
import os
from datetime import datetime
import pytz

KST = pytz.timezone('Asia/Seoul')
CONFIG_PATH = "data/config.json"
scheduler = AsyncIOScheduler()

def get_guild_configs():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

async def send_battleground_alert(bot):
    print(f"[{datetime.now()}] send_battleground_alert 호출됨")
    config = get_guild_configs()
    for guild in bot.guilds:
        guild_id = str(guild.id)
        if guild_id not in config:
            default_channel = guild.system_channel or next(
                (c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)
            if default_channel:
                config[guild_id] = {
                    "channel_id": default_channel.id,
                    "alerts": {
                        "battleground": True,
                        "subscription": True
                    }
                }
                save_config(config)

        setting = config.get(guild_id)
        if not setting or not setting.get("alerts", {}).get("battleground", True):
            continue

        channel_id = setting.get("channel_id")
        if not channel_id:
            continue
        channel = bot.get_channel(channel_id)
        if channel:
            embed = format_battleground_embed()
            await channel.send(embed=embed)

async def send_subscription_alert(bot):
    print(f"[{datetime.now()}] send_subscription_alert 호출됨")
    config = get_guild_configs()
    state, start, end = get_subscription_state()
    now = datetime.now(KST).replace(second=0, microsecond=0)
    기간_str = f"{start.strftime('%m월 %d일')} ~ {end.strftime('%m월 %d일')}"
    마감시간 = end.strftime('%m월 %d일 %H:%M')

    for guild in bot.guilds:
        guild_id = str(guild.id)
        if guild_id not in config:
            default_channel = guild.system_channel or next(
                (c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)
            if default_channel:
                config[guild_id] = {
                    "channel_id": default_channel.id,
                    "alerts": {
                        "battleground": True,
                        "subscription": True
                    }
                }
                save_config(config)

        setting = config.get(guild_id)
        if not setting or not setting.get("alerts", {}).get("subscription", True):
            continue

        channel_id = setting.get("channel_id")
        if not channel_id:
            continue
        channel = bot.get_channel(channel_id)
        if not channel:
            continue

        # 🔔 정확한 시작일 / 마감일 조건 추가
        if state == "청약 신청 기간":
            if now.date() == start.date() and now.hour == 0 and now.minute == 1:
                embed = generate_subscription_embed("신청 시작", 기간_str)
                await channel.send(embed=embed)

            elif now.date() == end.date() and now.hour == 23 and now.minute == 50:
                embed = generate_subscription_embed("신청 마감", 기간_str, 마감시간)
                await channel.send(embed=embed)

        elif state == "당첨 확인 기간":
            if now.date() == start.date() and now.hour == 0 and now.minute == 1:
                embed = generate_subscription_embed("당첨 확인 시작", 기간_str)
                await channel.send(embed=embed)

            elif now.date() == end.date() and now.hour == 23 and now.minute == 50:
                embed = generate_subscription_embed("당첨 마감", 기간_str, 마감시간)
                await channel.send(embed=embed)

def ensure_guild_config(guild_id: str, channel_id: int):
    config = get_guild_configs()
    if guild_id not in config:
        config[guild_id] = {
            "channel_id": channel_id,
            "alerts": {
                "battleground": True,
                "subscription": True
            }
        }
        save_config(config)

def start_schedulers(bot):
    scheduler.add_job(send_battleground_alert, "cron", hour=0, minute=0, args=[bot])
    scheduler.add_job(send_subscription_alert, "cron", hour="0,23", minute="1,50", args=[bot])
    scheduler.start()
