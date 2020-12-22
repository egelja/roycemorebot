import logging

from discord.ext import commands

from roycemorebot import constants

log = logging.getLogger(__name__)


# Change the bot class to log adding/removing cogs:
class CogLoggingBot(commands.Bot):
    """Subclass of `discord.ext.commands.Bot` to log adding and removing cogs."""

    def add_cog(self, cog: commands.Cog) -> None:
        """Add a cog and log it."""
        super().add_cog(cog)
        log.info(f"Cog loaded: {cog.qualified_name}")

    def remove_cog(self, name: str) -> None:
        """Remove a cog and log it."""
        super().remove_cog(name)
        log.info(f"Cog unloaded: {name}")


bot = CogLoggingBot(command_prefix=constants.Bot.prefix)


@bot.event
async def on_ready() -> None:
    """Message that the bot is ready."""
    log.info("We have logged in as {0.user}".format(bot))


@bot.command()
async def hello(ctx: commands.Context) -> None:
    """Responder to `hello` message."""
    await ctx.send("Hello!")

bot.run(constants.Bot.bot_token)
