import logging
from datetime import datetime

from discord import Embed
from discord.ext import commands

PRECISION = 3

log = logging.getLogger(__name__)


class Status(commands.Cog):
    """Status commands for the bot."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        """Send the latency of the bot."""
        raw_bot_latency = (
            datetime.utcnow() - ctx.message.created_at
        ).total_seconds() * 1000
        log.info(f"Now: {datetime.utcnow()}, Message creation: {ctx.message.created_at}")
        bot_latency = f"{raw_bot_latency:.{PRECISION}f} ms"
        api_latency = f"{self.bot.latency * 1000:.{PRECISION}f} ms"

        embed = Embed(title="Pong!")
        embed.add_field(name="Bot latency:", value=bot_latency, inline=False)
        embed.add_field(name="Discord API Latency:", value=api_latency, inline=False)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Add the status cog."""
    bot.add_cog(Status(bot))
