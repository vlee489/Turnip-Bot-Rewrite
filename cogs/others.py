"""
Contains all the other commands that have no specific
home.
"""
from discord.ext import commands
import pyjokes
import numpy
import os
from dotenv import load_dotenv
import json
import utils

load_dotenv(".env")

petPicNumber = 65


class Others(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.CDNLink = os.environ.get("CDNLink")

    @commands.command(name='joke',
                      help="Get a random programmer joke.")
    async def joke(self, ctx):
        joke = pyjokes.get_joke()
        embedded = await utils.create_embed("Joke", joke)
        embedded.set_footer(text="Jokes from pyjok.es", icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        await ctx.send(embed=embedded)

    @commands.command(name='credits',
                      help="The credits for the bot")
    async def credits(self, ctx):
        embedded = await utils.create_embed("Credits", 'Credits of Turnip bot',
                                            'https://github.com/vlee489/Turnip-Bot/wiki/Credits')
        embedded.set_footer(text="Turnip Bot by vlee489", icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        await ctx.send(embed=embedded)

    @commands.command(name='add',
                      help="Add the bot to your own server")
    async def add(self, ctx):
        embedded = await utils.create_embed("Turnip Bot", 'Add Turnip Bot Here',
                                            "https://github.com/vlee489/Turnip-Bot/")
        embedded.set_footer(text="Turnip Bot by vlee489", icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        await ctx.send(embed=embedded)

    @commands.command(name='stats',
                      help="Gets the stats & support for the bot")
    async def stats(self, ctx):
        embedded = await utils.create_embed(title='Turnip Bot Stats', url='https://github.com/vlee489/Turnip-Bot/')
        embedded.add_field(name="Version:", value="Alpha 9.0 RC2", inline=True)
        embedded.add_field(name="Latency:", value="{}ms".format(round(self.bot.latency * 1000, 2)), inline=True)
        embedded.add_field(name="Used in number of servers:", value="{} servers".format(len(self.bot.guilds)),
                           inline=False)
        embedded.add_field(name="Contributors:", value="2", inline=False)
        embedded.add_field(name="Kofi Donations", value="https://ko-fi.com/vlee489", inline=False)
        embedded.add_field(name="Issues report", value="https://github.com/vlee489/Turnip-Bot/issues", inline=False)
        embedded.add_field(name="Discord Support Server", value="https://discord.gg/JPrC6c2", inline=False)
        embedded.set_footer(text="Turnip Bot by vlee489", icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        await ctx.send(embed=embedded)

    @commands.command(name='pet', help="Get a picture of a pet",
                      pass_context=True)
    async def pet(self, ctx):
        embedded = await utils.create_embed(title="Pets!", url="https://github.com/vlee489/Turnip-Bot/wiki/Credits")
        ran = numpy.random.randint(0, petPicNumber)
        embedded.set_image(url="{}/TurnipBot/pets/{}.png".format(self.CDNLink, ran))
        embedded.set_footer(text="Turnip Bot | Picture No.{}".format(ran),
                            icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
        await ctx.send(embed=embedded)

    @commands.command(name='changePrefix', help="Change the command prefix for this server\n"
                                                "<newPrefix>: This is the prefix you now want to use",
                      pass_context=True, aliases=['changeprefix'])
    async def changePrefix(self, ctx, newPrefix):
        if ctx.message.author.id == ctx.message.guild.owner.id:
            with open('prefix.json', 'r') as prefixFile:
                prefixes = json.load(prefixFile)
            prefixes[str(ctx.guild.id)] = newPrefix
            with open('prefix.json', 'w') as prefixFile:
                json.dump(prefixes, prefixFile, indent=4)
            await ctx.send("Prefix for Turnip Bot has been changed to `{}` for this server".format(newPrefix))
        else:
            await ctx.send("Error: Prefix can only be changed by server owner!")


def setup(bot):
    bot.add_cog(Others(bot))
