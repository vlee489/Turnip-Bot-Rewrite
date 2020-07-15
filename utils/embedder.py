import discord
import datetime


async def create_embed(title=None, description=None, url=None, date=datetime.datetime.utcnow()) -> discord.Embed:
    """
    Creates a discord embed template
    :param title: str
        Title for embed
    :param description: str
        Description for embed
    :param url: str
        URL for embed
    :return: discord.embed
        discord.py embed object
    """
    embed = discord.Embed(title=title, description=description, url=url, color=0xCF70D3)
    embed.set_author(name="Turnip Bot",
                     url="https://github.com/vlee489/Turnip-Bot/",
                     icon_url="https://cdn.vlee.me.uk/TurnipBot/icon.png")
    embed.timestamp = date
    return embed


async def list_to_code_block(message: list) -> str:
    """
    Turns a list into a code block with each item on a new line in a list with a -
    :param message: list
        List to turn into code block
    :return: str
        Str code block
    """
    codeBlock = "```\n"
    for items in message:
        codeBlock = codeBlock + "- {}\n".format(items)
    return codeBlock + "```"
