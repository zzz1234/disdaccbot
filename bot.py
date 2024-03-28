# bot.py
import os
import sys

import discord
from dotenv import load_dotenv
import traceback

from discord.ext import commands

load_dotenv('local_env')
TOKEN = os.getenv('DISCORD_TOKEN')

# Define your intents
intents = discord.Intents.all()
# Add specific intents you need (e.g., messages, members, reactions)
intents.messages = True
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

initial_extensions = [
    'cogs.utility',
    'cogs.quote',
    'cogs.challenges',
    'cogs.quiz'  # Add more cogs here if needed
]

# Load cogs
async def load_cogs():
    for extension in initial_extensions:
        try:
            await client.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name} ({client.user.id})")
    print("------")
    await load_cogs()

client.run(TOKEN)