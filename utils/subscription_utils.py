from datetime import datetime, timedelta
import pytz
import discord

KST = pytz.timezone("Asia/Seoul")
BASE_DATE = datetime(2025, 5, 2, tzinfo=KST)  # 당첨 확인 시작일


def get_subscription_state(now=None):
    if now is None:
        now = datetime.now(KST)

    days_passed = (now - BASE_DATE).days
    cycle_day = days_passed % 9

    if cycle_day in [0, 1, 2, 3]:  # 당첨 확인 (4일)
        start = BASE_DATE + timedelta(days=days_passed - cycle_day)
        end = start + timedelta(days=3)
        return "당첨 확인 기간", start, end
    else:  # 신청 (5일)
        start = BASE_DATE + timedelta(days=days_passed - cycle_day + 4)
        end = start + timedelta(days=4)
        return "청약 신청 기간", start, end


def generate_subscription_embed(state_type: str,
                                기간_str: str,
                                마감시간_str: str = None):
    if state_type == "신청 시작":
        return discord.Embed(title="📝 청약 신청 접수 개시!",
                             description=("✨ 꿈에 그리던 기회가 찾아왔습니다!\n"
                                          "이제 청약 신청이 **시작**되었습니다.\n\n"
                                          f"📅 신청 기간: **{기간_str}**\n"
                                          "📌 놓치지 말고 꼭 참여하세요!"),
                             color=discord.Color.green())

    elif state_type == "신청 마감":
        return discord.Embed(title="🚨 청약 신청 마감 임박!",
                             description=("⏰ *지금 신청 안 하면 후회할지도...?!*\n"
                                          f"신청 마감까지 **단 10분!**\n\n"
                                          f"📅 신청 마감: **{마감시간_str}**\n"
                                          "💨 서둘러주세요, 기회는 자정까지!"),
                             color=discord.Color.red())

    elif state_type == "당첨 확인 시작":
        return discord.Embed(title="🎯 청약 당첨 확인 시작!",
                             description=("🎉 당신의 운명을 확인할 시간입니다!\n"
                                          "**청약 당첨 확인이 시작**되었습니다.\n\n"
                                          f"📅 확인 기간: **{기간_str}**\n"
                                          "📌 놓치지 마세요!"),
                             color=discord.Color.blue())

    elif state_type == "당첨 마감":
        return discord.Embed(title="⏳ 당첨 확인 종료 임박!",
                             description=("⚠️ *10분 후, 확인 기회 종료!*\n"
                                          f"당첨 확인 마감까지 남은 시간: **10분**\n\n"
                                          f"📅 마감 시간: **{마감시간_str}**\n"
                                          "💥 놓치면 당신의 길이!!!!"),
                             color=discord.Color.orange())

    elif state_type == "상태 조회":
        신청, 확인 = 기간_str.split("|")
        return discord.Embed(
            title="📋 청약 일정 안내",
            description="📌 현재 청약 진행 상태를 안내해드립니다.",
            color=discord.Color.purple()
        ).add_field(name="📆 신청 기간", value=신청, inline=False)\
         .add_field(name="📆 당첨 확인", value=확인, inline=False)\
         .set_footer(text="⏰ 청약 주기는 4일(확인) + 5일(신청)입니다.")

    else:
        return discord.Embed(title="❓ 알 수 없는 상태", description="지원되지 않는 상태입니다.")
