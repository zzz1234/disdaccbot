import json
import random
from discord.ext import commands

class Challenges(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready!')

    @commands.command()
    async def challenge(self, ctx):
        # Read Json file challenges.json
        with open('data/challenges.json') as f:
            challenges = json.load(f)
        rand_challenge = random.choice(challenges['challenges'])
        await ctx.send(f"{rand_challenge['name']} - {rand_challenge['url']}")

async def setup(bot):
    await bot.add_cog(Challenges(bot))