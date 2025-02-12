import discord
from discord.ext import commands
import pyautogui
from io import BytesIO
import logging
import os

# Debug Mode
DEBUG_MODE = False

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True

# Disable the default help command
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Replace these with your actual keys and IDs
CHANNEL_ID = 1329249832732327999
BOT_TOKEN = 'MTMyOTI0ODc2MDczOTQwMTc2OQ.GPJhEA.QWGMX3YBKxTEKVtNLuYdRCOiMY6vdWThLnexgE'

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global check to restrict commands to the specified channel
@bot.check
def is_correct_channel(ctx):
    return ctx.channel.id == CHANNEL_ID

# Bot Events and Commands
@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Meraxes has risen from slumber.")
    else:
        print("Channel not found. Check the CHANNEL_ID.")

@bot.command(name="screenshot", aliases=["ss"])
async def screenshot(ctx):
    """Capture a screenshot."""
    screenshot = pyautogui.screenshot()
    img_byte_arr = BytesIO()
    screenshot.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    await ctx.send(file=discord.File(img_byte_arr, filename='screenshot.png'))

# Start the bot
bot.run(BOT_TOKEN)
