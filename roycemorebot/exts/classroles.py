import discord
from discord.ext import commands

from roycemorebot.constants import ClassRoles as CRoles  # noqa: F401


class ClassRoles(commands.Cog):
    """User-assigned roles based on their grad."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def freshmen(self, ctx: commands.Context, user: discord.Member = None):
        if user is None:
            user = ctx.author
        # elif user != ctx.author and ctx.author


def setup(bot: commands.Bot) -> None:
    """Add the ClassRoles cog to the bot."""
    bot.add_cog(ClassRoles(bot))
