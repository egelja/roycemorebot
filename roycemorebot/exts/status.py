import logging
from datetime import datetime

from discord import Colour, Embed
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
        bot_latency = f"{raw_bot_latency:.{PRECISION}f} ms"
        raw_api_latency = self.bot.latency * 1000
        api_latency = f"{raw_api_latency:.{PRECISION}f} ms"

        if (raw_bot_latency <= 100 and raw_api_latency <= 100):
            embed = Embed(title="Pong!", colour=Colour.green())
        elif (raw_bot_latency <= 250 and raw_api_latency <= 250):
            embed = Embed(title="Pong!", colour=Colour.orange())
        else:
            embed = Embed(title="Pong!", colour=Colour.red())

        embed.add_field(name="Bot latency:", value=bot_latency, inline=False)
        embed.add_field(name="Discord API Latency:", value=api_latency, inline=False)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Add the status cog."""
    bot.add_cog(Status(bot))
