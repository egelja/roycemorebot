import discord
from discord.ext import commands

from roycemorebot.checks import has_no_roles_check
from roycemorebot.constants import ClassRoles as CRoles
from roycemorebot.constants import MOD_ROLES


class ClassRoles(commands.Cog):
    """User-assigned roles based on their grade."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["fm", "freshmen"])
    async def freshman(
        self, ctx: commands.Context, user: discord.Member = None
    ) -> None:
        """Give a freshman the `Freshmen` role."""
        if user is None:
            user = ctx.author

        elif user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await ctx.send("You cannot assign a user other than yourself a class role.")
            return

        await user.add_roles(discord.Object(CRoles.freshmen), reason="Class Roles")

    @commands.command(aliases=["sm", "sophomores"])
    async def sophomore(
        self, ctx: commands.Context, user: discord.Member = None
    ) -> None:
        """Give a sophomore the `Sophomore` role."""
        if user is None:
            user = ctx.author

        elif user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await ctx.send("You cannot assign a user other than yourself a class role.")
            return

        await user.add_roles(discord.Object(CRoles.sophomores), reason="Class Roles")

    @commands.command(aliases=["jr", "juniors"])
    async def junior(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a junior the `Junior` role."""
        if user is None:
            user = ctx.author

        elif user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await ctx.send("You cannot assign a user other than yourself a class role.")
            return

        await user.add_roles(discord.Object(CRoles.juniors), reason="Class Roles")

    @commands.command(aliases=["sn", "seniors"])
    async def senior(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a senior the `Senior` role."""
        if user is None:
            user = ctx.author

        elif user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await ctx.send("You cannot assign a user other than yourself a class role.")
            return

        await user.add_roles(discord.Object(CRoles.seniors), reason="Class Roles")

    @commands.command(aliases=["al", "alumni"])
    async def alum(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a alum the `Alumni` role."""
        if user is None:
            user = ctx.author

        elif user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await ctx.send("You cannot assign a user other than yourself a class role.")
            return

        await user.add_roles(discord.Object(CRoles.alumni), reason="Class Roles")


def setup(bot: commands.Bot) -> None:
    """Add the ClassRoles cog to the bot."""
    bot.add_cog(ClassRoles(bot))
