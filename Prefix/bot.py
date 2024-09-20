# DO NOT TOUCH THE IMPORTS IF YOU DO NOT KNOW WHAT YOU ARE DOING
import discord
from discord.ext import commands
import os
import json

intents = discord.Intents.all()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# If no config file exists it will write this into a new config.json
default_settings = {
    "token": "YOUR_BOT_TOKEN_HERE"
}

# Ensure config.json exists and create it with default settings if it doesn't
if not os.path.exists("config.json"):
    with open("config.json", "w") as config_file:
        json.dump(default_settings, config_file, indent=4)
    print("config.json not found. Created default config.json. Please update it with your bot token and owner ID.")
else:
    print("config.json exists. Loading settings...")

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    token = config["token"]

banner = r"""
        _ _  _ ____ ___ ____ _  _ ___ _  _ ____ _  _ ____
        | |\ | [__   |  |__| |\ |  |  |\ | |__| |\/| |___
        | | \| ___]  |  |  | | \|  |  | \| |  | |  | |___
"""

@bot.event
async def on_ready():
    print("        =================================================")
    print(f"{banner}")
    print("============================================================")
    print(f"[Bot name] Bot V[Version] Loaded as: {bot.user}!")
    print("============================================================")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="InstantName"))

#========================================================================================================================================
# Bot commands:

@bot.command(name='clear')
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    if amount <= 0:
        await ctx.send("Please specify a number greater than 0.")
    else:
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"Deleted {len(deleted)} messages.", delete_after=5)

@bot.command(name='say')
@commands.has_permissions(administrator=True)
async def say(ctx, channel: discord.TextChannel, *, message: str):
    await channel.send(message)
    await ctx.send(f"Message sent to {channel.mention}", delete_after=5)

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message) and not message.author.guild_permissions.administrator:
        await message.channel.send(f"Do not tag me 🖕 {message.author.mention}")
    await bot.process_commands(message)

@clear.error
@say.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}, you don't have permission to do that!", delete_after=5)
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Please provide a valid number of messages or valid channel.", delete_after=5)

bot.run(token)