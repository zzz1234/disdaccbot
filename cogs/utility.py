import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready!')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Hello! I am your friendly Discord bot. {ctx.author.mention}")

async def setup(bot):
    await bot.add_cog(Utility(bot))