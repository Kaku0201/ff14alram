print(f"[LOAD] test.py ({__file__})")

from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Test(bot))
