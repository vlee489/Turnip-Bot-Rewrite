"""
This file starts and runs the main bot functions
"""
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import random
import datetime
import utils
import json

load_dotenv("configs/.env")
TOKEN = os.environ.get("discord_token")
prefixFileLocation = "configs/prefix.json"

# This is the list of cogs that discord.py loads in as file names without the .py extension
extensions = [
    "cogs.other",
    "cogs.topgg"
]

presence_strings = [
    "Come and get your turnips!"
]

helloMessage = "Hello There :wave:, use `<help` to get started"
if os.path.exists("join.txt"):
    with open("join.txt", 'r') as f:
        helloMessage = f.read()


# Gets the prefix for the servers
def getPrefix(client, message):
    """
    Gets the prefix for commands for servers
    :param client: client
        Client object
    :param message: message
        message object
    :return: str
        Prefix of the server/DM
    """
    if isinstance(message.channel, discord.DMChannel):
        return commands.when_mentioned_or("<")(bot, message)
    with open(prefixFileLocation, 'r') as prefixFile:
        prefixes = json.load(prefixFile)
    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix=getPrefix)


@bot.event
async def on_guild_join(guild):
    # This adds the prefix to the file
    with open(prefixFileLocation, 'r') as prefixFile:
        prefixes = json.load(prefixFile)
    prefixes[str(guild.id)] = "<"
    with open(prefixFileLocation, 'w') as prefixFile:
        json.dump(prefixes, prefixFile, indent=4)
    # Send the hello message
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(helloMessage)
            break


@bot.event
async def on_guild_remove(guild):
    # Removed guild from prefix file if bot is removed
    with open(prefixFileLocation, 'r') as prefixFile:
        prefixes = json.load(prefixFile)
    prefixes.pop(str(guild.id))
    with open(prefixFileLocation, 'w') as prefixFile:
        json.dump(prefixes, prefixFile, indent=4)


# Handles incorrect input from user
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing data, you got got to enter something after the command!\n"
                       "You can use `<help` for help")
    elif isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRole):
        return
    elif isinstance(error, commands.TooManyArguments):
        return
    else:
        utils.errorCollector.collect_error(error, "on_command_error")


# When the bot is loaded
@bot.event
async def on_ready():
    print('Logged in as:')
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    print("Booted up at: {}".format(datetime.datetime.utcnow()))
    print("Used in {} servers".format(len(bot.guilds)))
    print('------')
    bot.loop.create_task(presence_update())


# Updates presence data
async def presence_update():
    while True:
        await bot.change_presence(activity=discord.Game(random.choice(presence_strings)))
        await asyncio.sleep(60)

# Runs the whole show
if __name__ == "__main__":
    for extension in extensions:
        try:
            # Loads in cogs
            bot.load_extension(extension)
            print("Loaded cog: {}".format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(TOKEN)

