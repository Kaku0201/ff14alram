from datetime import datetime, timedelta
import pytz
import discord

KST = pytz.timezone("Asia/Seoul")

BATTLEGROUNDS = [("온살 하카이르", "계절끝 합전"), ("봉인된 바위섬", "쟁탈전"), ("영광의 평원", "쇄빙전")]

BASE_DATE = datetime(2025, 5, 5, tzinfo=KST)  # 온살 시작일


def get_battleground_info():
    today = datetime.now(KST).date()
    days_passed = (today - BASE_DATE.date()).days
    today_idx = days_passed % 3
    tomorrow_idx = (today_idx + 1) % 3
    day_after_idx = (today_idx + 2) % 3

    return {
        "today": BATTLEGROUNDS[today_idx],
        "tomorrow": BATTLEGROUNDS[tomorrow_idx],
        "day_after": BATTLEGROUNDS[day_after_idx],
        "date": today.strftime("%m월 %d일")
    }


def format_battleground_embed():
    info = get_battleground_info()
    today_name, today_type = info["today"]
    tomorrow_name, tomorrow_type = info["tomorrow"]
    day_after_name, day_after_type = info["day_after"]

    embed = discord.Embed(
        title="⚔️ 전장 통신 개방 중...",
        description=f"📍 **오늘의 작전지**: {today_name} ({today_type})",
        color=discord.Color.red())

    embed.add_field(name="📢 작전 명령",
                    value="⚠️ 모험가님, 출정을 준비하세요! 승리는 당신의 손에 달려 있습니다.",
                    inline=False)

    embed.add_field(name="📅 향후 전장 일정",
                    value=(f"- 내일: **{tomorrow_name} ({tomorrow_type})**\n"
                           f"- 모레: **{day_after_name} ({day_after_type})**"),
                    inline=False)

    embed.set_footer(text="🕛 전장은 매일 자정에 변경됩니다.")

    return embed
