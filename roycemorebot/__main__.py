import logging
import os

from discord.ext import commands

from roycemorebot import constants

log = logging.getLogger(__name__)


# Change the bot class to log adding/removing cogs:
class CogLoggingBot(commands.Bot):
    """Subclass of `discord.ext.commands.Bot` to log adding and removing cogs."""

    def add_cog(self, cog) -> None:  # noqa: ANN001
        """Add a cog and log it."""
        super().add_cog(cog)
        log.info(f"Cog loaded: {cog.qualified_name}")

    def remove_cog(self, name) -> None:  # noqa: ANN001
        """Remove a cog and log it."""
        super().remove_cog(name)
        log.info(f"Cog unloaded: {name}")


# Create bot
bot = CogLoggingBot(command_prefix=constants.Bot.prefix)


# Message when bot is ready
@bot.event
async def on_ready() -> None:
    """Message that the bot is ready."""
    log.info(f"We have logged in as {bot.user}")


# Load cogs
for file in os.listdir(os.path.join(".", "roycemorebot", "exts")):
    if file.endswith(".py") and not file.startswith("_"):
        bot.load_extension(f"roycemorebot.exts.{file[:-3]}")


@bot.command()
async def reload(ctx: commands.Context, cog: str) -> None:
    """Reload a cog."""
    try:
        bot.unload_extension(cog)
        bot.load_extension(cog)
    except commands.ExtensionNotLoaded:
        await ctx.send(f"Could not find the extension `{cog}`!")
    else:
        await ctx.send(f"Cog `{cog}` successfully reloaded!")


bot.run(constants.Bot.bot_token)
