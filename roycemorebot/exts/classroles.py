import discord
from discord.ext import commands

from roycemorebot.checks import has_any_role_check, has_no_roles_check
from roycemorebot.constants import CLASS_ROLES, MOD_ROLES
from roycemorebot.constants import ClassRoles as CRoles


class ClassRoles(commands.Cog):
    """User-assigned roles based on their grade."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["fm", "freshmen"])
    async def freshman(
        self, ctx: commands.Context, user: discord.Member = None
    ) -> None:
        """Give a freshman the `Freshmen` role."""
        # Default to the user being the author
        if user is None:
            user = ctx.author
        # Check if the user is not a mod and they tried to give someone else a role.
        if user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await ctx.send("You cannot assign a user other than yourself a class role.")
            return
        elif user != ctx.author and await has_any_role_check(ctx, *MOD_ROLES):
            for role in CLASS_ROLES:
                await user.remove_roles(discord.Object(role), reason="Mod Replacing Class Roles")

        # Check if the user is self-roleing and already has a class role.
        if user == ctx.author and await has_any_role_check(ctx, *CLASS_ROLES):
            await ctx.send(
                "You already have a class role. If you mistakenly assigned the wrong role, contact <@575252669443211264>."
            )
            return

        await user.add_roles(discord.Object(CRoles.freshmen), reason="Class Roles")

    @commands.command(aliases=["sm", "sophomores"])
    async def sophomore(
        self, ctx: commands.Context, user: discord.Member = None
    ) -> None:
        """Give a sophomore the `Sophomore` role."""
        if user is None:
            user = ctx.author

        if user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await ctx.send("You cannot assign a user other than yourself a class role.")
            return
        elif user != ctx.author and await has_any_role_check(ctx, *MOD_ROLES):
            for role in CLASS_ROLES:
                await user.remove_roles(discord.Object(role), reason="Mod Replacing Class Roles")

        # Check if the user is self-roleing and already has a class role.
        if user == ctx.author and await has_any_role_check(ctx, *CLASS_ROLES):
            await ctx.send(
                "You already have a class role. If you mistakenly assigned the wrong role, contact <@575252669443211264>."
            )
            return

        await user.add_roles(discord.Object(CRoles.sophomores), reason="Class Roles")

    @commands.command(aliases=["jr", "juniors"])
    async def junior(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a junior the `Junior` role."""
        if user is None:
            user = ctx.author

        if user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await ctx.send("You cannot assign a user other than yourself a class role.")
            return
        elif user != ctx.author and await has_any_role_check(ctx, *MOD_ROLES):
            for role in CLASS_ROLES:
                await user.remove_roles(discord.Object(role), reason="Mod Replacing Class Roles")

        # Check if the user is self-roleing and already has a class role.
        if user == ctx.author and await has_any_role_check(ctx, *CLASS_ROLES):
            await ctx.send(
                "You already have a class role. If you mistakenly assigned the wrong role, contact <@575252669443211264>."
            )
            return

        await user.add_roles(discord.Object(CRoles.juniors), reason="Class Roles")

    @commands.command(aliases=["sr", "seniors"])
    async def senior(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a senior the `Senior` role."""
        if user is None:
            user = ctx.author

        if user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await ctx.send("You cannot assign a user other than yourself a class role.")
            return
        elif user != ctx.author and await has_any_role_check(ctx, *MOD_ROLES):
            for role in CLASS_ROLES:
                await user.remove_roles(discord.Object(role), reason="Mod Replacing Class Roles")

        # Check if the user is self-roleing and already has a class role.
        if user == ctx.author and await has_any_role_check(ctx, *CLASS_ROLES):
            await ctx.send(
                "You already have a class role. If you mistakenly assigned the wrong role, contact <@575252669443211264>."
            )
            return

        await user.add_roles(discord.Object(CRoles.seniors), reason="Class Roles")

    @commands.command(aliases=["al", "alumni"])
    async def alum(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a alum the `Alumni` role."""
        if user is None:
            user = ctx.author

        if user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await ctx.send("You cannot assign a user other than yourself a class role.")
            return
        elif user != ctx.author and await has_any_role_check(ctx, *MOD_ROLES):
            for role in CLASS_ROLES:
                await user.remove_roles(discord.Object(role), reason="Mod Replacing Class Roles")

        # Check if the user is self-roleing and already has a class role.
        if user == ctx.author and await has_any_role_check(ctx, *CLASS_ROLES):
            await ctx.send(
                "You already have a class role. If you mistakenly assigned the wrong role, contact <@575252669443211264>."
            )
            return

        await user.add_roles(discord.Object(CRoles.alumni), reason="Class Roles")


def setup(bot: commands.Bot) -> None:
    """Add the ClassRoles cog to the bot."""
    bot.add_cog(ClassRoles(bot))
