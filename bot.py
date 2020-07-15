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

load_dotenv("configs/.env")
TOKEN = os.environ.get("discord_token")

# This is the list of cogs that discord.py loads in as file names without the .py extension
extensions = [
    "cogs.other"
]

presence_strings = [
    "Come and get your turnips!"
]

bot = commands.Bot("<")


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

