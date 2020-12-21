import logging

import discord
from discord import Message

from roycemorebot import constants

client = discord.Client()

log = logging.getLogger(__name__)


@client.event
async def on_ready() -> None:
    """Message that the bot is ready."""
    log.info("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message: Message) -> None:
    """Message responder."""
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


client.run(constants.TOKEN)
