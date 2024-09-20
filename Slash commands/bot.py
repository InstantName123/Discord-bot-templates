# DO NOT TOUCH THE IMPORTS IF YOU DO NOT KNOW WHAT YOU ARE DOING
import discord
from discord.ext import commands
import os
import json

intents = discord.Intents.all()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="/", intents=intents)

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

@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Synced slash commands.")

#========================================================================================================================================
# Bot commands:

@bot.slash_command(name="clear", description="Clears a specified number of messages from the channel.")
async def clear(ctx: discord.ApplicationContext, amount: int):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        return
    if amount < 1:
        await ctx.respond("You must delete at least one message.", ephemeral=True)
        return
    messages = await ctx.channel.history(limit=amount + 1).flatten()
    for message in messages:
        await message.delete()

    await ctx.respond(f"Deleted {amount} messages.", ephemeral=True)

@bot.slash_command(name="say", description="Send a message to a specified channel")
async def say(ctx: discord.ApplicationContext, channel: discord.TextChannel, message: str):
    if ctx.author.guild_permissions.administrator:
        await channel.send(message)
        await ctx.respond(f"Message sent to {channel.mention}", ephemeral=True)
    else:
        await ctx.respond("You have no access to this command.", ephemeral=True)

@bot.event
async def on_message(message: discord.Message):
    if bot.user in message.mentions:
        if not message.author.guild_permissions.administrator:
            response = await message.channel.send("Do not tag me 🖕")
            await message.delete(delay=5)
            await response.delete(delay=5)
        else:
            response2 = await message.channel.send("Hey there boss!")
            await message.delete(delay=5)
            await response2.delete(delay=5)

    await bot.process_commands(message)

bot.run(token)