print(f"[LOAD] main.py ({__file__})")

from scheduler_module import start_schedulers
import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from keep_alive import keep_alive

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message(
            "❗이 명령어는 **관리자만 사용할 수 있어요!**", ephemeral=True)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print(f"✅ Synced slash commands globally.")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")

async def load_extensions():
    await bot.load_extension("cogs.battleground")
    await bot.load_extension("cogs.subscription")
    await bot.load_extension("cogs.settings")
    await bot.load_extension("cogs.test")

async def main():
    keep_alive()
    await load_extensions()
    start_schedulers(bot)
    await bot.start(os.environ['TOKEN'])

if __name__ == "__main__":
    asyncio.run(main())
