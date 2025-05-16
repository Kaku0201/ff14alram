import discord
from discord import app_commands
from discord.ext import commands
import json
import os

CONFIG_PATH = "data/config.json"

def ensure_config_file():
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f)

def load_config():
    ensure_config_file()  # 없으면 자동 생성
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

class Settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="채널설정",
                          description="현재 채널을 알림 채널로 등록 또는 해제합니다.")
    @app_commands.checks.has_permissions(administrator=True)
    async def 채널설정(self, interaction: discord.Interaction):
        config = load_config()
        guild_id = str(interaction.guild.id)
        channel_id = interaction.channel.id
        channel_name = interaction.channel.mention

        if guild_id in config and config[guild_id].get(
                "channel_id") == channel_id:
            config[guild_id]["channel_id"] = None
            save_config(config)
            embed = discord.Embed(
                title="❌ 알림 채널 해제",
                description=f"{channel_name} 채널이 더 이상 알림 채널로 사용되지 않습니다.",
                color=discord.Color.red())
        else:
            config.setdefault(guild_id, {})["channel_id"] = channel_id
            config[guild_id].setdefault("alerts", {
                "battleground": True,
                "subscription": True
            })
            save_config(config)
            embed = discord.Embed(
                title="✅ 알림 채널 등록 완료",
                description=f"{channel_name} 채널이 이제 알림 채널로 사용됩니다.",
                color=discord.Color.green())

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="알림설정",
                          description="전장 또는 청약 알림의 활성화 여부를 설정합니다.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(
        알림종류=[
            app_commands.Choice(name="전장", value="전장"),
            app_commands.Choice(name="청약", value="청약"),
        ]
    )
    @app_commands.describe(활성화여부="켜기(True) 또는 끄기(False) 중 선택")
    async def 알림설정(self, interaction: discord.Interaction,
                     알림종류: app_commands.Choice[str], 활성화여부: bool):
        종류_맵 = {"청약": "subscription", "전장": "battleground"}

        if 알림종류.value not in 종류_맵:
            embed = discord.Embed(title="❗ 잘못된 알림 종류",
                                  description="`청약` 또는 `전장` 중 하나만 선택하세요.",
                                  color=discord.Color.orange())
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)
            return

        알림코드 = 종류_맵[알림종류.value]
        config = load_config()
        guild_id = str(interaction.guild.id)
        config.setdefault(guild_id, {"channel_id": None, "alerts": {}})
        config[guild_id]["alerts"][알림코드] = 활성화여부
        save_config(config)

        상태 = "활성화됨 ✅" if 활성화여부 else "비활성화됨 ❌"

        embed = discord.Embed(
            title=f"🔔 {알림종류.value} 알림 설정 변경",
            description=f"`{알림종류.value}` 알림이 **{상태}** 상태로 설정되었습니다.",
            color=discord.Color.blue() if 활성화여부 else discord.Color.dark_gray())

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Settings(bot))
