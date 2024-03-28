import random
from utils.api_requests import get_api_response

import discord
from discord.ext import commands

class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready!')

    @commands.command()
    async def quote(self, ctx):
        random_number = random.randint(1, 1000)
        url = "https://dummyjson.com/quotes/" + str(random_number)
        response = get_api_response(url)
        quote = response["quote"]
        author = response["author"]
        await ctx.send(f"{quote} - {author}")

async def setup(bot):
    await bot.add_cog(Quote(bot))