import logging

import discord
from discord.ext import commands

from roycemorebot.checks import has_any_role_check, has_no_roles_check
from roycemorebot.constants import CLASS_ROLES, MOD_ROLES
from roycemorebot.constants import ClassRoles as CRoles

log = logging.getLogger(__name__)


class ClassRoles(commands.Cog, name="Class Roles"):
    """User-assigned roles based on their grade."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=("fm", "freshmen"))
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
            log.info(
                f"Replacing {user}'s class roles at request of moderator {ctx.author}"
            )
            for role in CLASS_ROLES:
                await user.remove_roles(
                    discord.Object(role),
                    reason=f"Moderator {ctx.author} Replacing {user}'s Class Roles",
                )

        # Check if the user is self-roleing and already has a class role.
        if user == ctx.author and await has_any_role_check(ctx, *CLASS_ROLES):
            modmail = discord.utils.get(ctx.guild.members, id=575252669443211264)
            await ctx.send(
                f"You already have a class role. If you mistakenly assigned the wrong role, contact {modmail.mention}."
            )
            return

        await user.add_roles(discord.Object(CRoles.freshmen), reason="Class Roles")
        log.trace(f"Assigned {user} the Freshmen role")

    @commands.guild_only()
    @commands.command(aliases=("sm", "sophomores"))
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
            log.info(
                f"Replacing {user}'s class roles at request of moderator {ctx.author}"
            )
            for role in CLASS_ROLES:
                await user.remove_roles(
                    discord.Object(role),
                    reason=f"Moderator {ctx.author} Replacing {user}'s Class Roles",
                )

        # Check if the user is self-roleing and already has a class role.
        if user == ctx.author and await has_any_role_check(ctx, *CLASS_ROLES):
            modmail = discord.utils.get(ctx.guild.members, id=575252669443211264)
            await ctx.send(
                f"You already have a class role. If you mistakenly assigned the wrong role, contact {modmail.mention}."
            )
            return

        await user.add_roles(discord.Object(CRoles.sophomores), reason="Class Roles")
        log.trace(f"Assigned {user} the Sophomore role")

    @commands.guild_only()
    @commands.command(aliases=("jr", "juniors"))
    async def junior(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a junior the `Junior` role."""
        if user is None:
            user = ctx.author

        if user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await ctx.send("You cannot assign a user other than yourself a class role.")
            return
        elif user != ctx.author and await has_any_role_check(ctx, *MOD_ROLES):
            log.info(
                f"Replacing {user}'s class roles at request of moderator {ctx.author}"
            )
            for role in CLASS_ROLES:
                await user.remove_roles(
                    discord.Object(role),
                    reason=f"Moderator {ctx.author} Replacing {user}'s Class Roles",
                )

        # Check if the user is self-roleing and already has a class role.
        if user == ctx.author and await has_any_role_check(ctx, *CLASS_ROLES):
            modmail = discord.utils.get(ctx.guild.members, id=575252669443211264)
            await ctx.send(
                f"You already have a class role. If you mistakenly assigned the wrong role, contact {modmail.mention}."
            )
            return

        await user.add_roles(discord.Object(CRoles.juniors), reason="Class Roles")
        log.trace(f"Assigned {user} the Junior role")

    @commands.guild_only()
    @commands.command(aliases=("sr", "seniors"))
    async def senior(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a senior the `Senior` role."""
        if user is None:
            user = ctx.author

        if user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await ctx.send("You cannot assign a user other than yourself a class role.")
            return
        elif user != ctx.author and await has_any_role_check(ctx, *MOD_ROLES):
            log.info(
                f"Replacing {user}'s class roles at request of moderator {ctx.author}"
            )
            for role in CLASS_ROLES:
                await user.remove_roles(
                    discord.Object(role),
                    reason=f"Moderator {ctx.author} Replacing {user}'s Class Roles",
                )

        # Check if the user is self-roleing and already has a class role.
        if user == ctx.author and await has_any_role_check(ctx, *CLASS_ROLES):
            modmail = discord.utils.get(ctx.guild.members, id=575252669443211264)
            await ctx.send(
                f"You already have a class role. If you mistakenly assigned the wrong role, contact {modmail.mention}."
            )
            return

        await user.add_roles(discord.Object(CRoles.seniors), reason="Class Roles")
        log.trace(f"Assigned {user} the Senior role")

    @commands.guild_only()
    @commands.command(aliases=("al", "alumni"))
    async def alum(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a alum the `Alumni` role."""
        if user is None:
            user = ctx.author

        if user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await ctx.send("You cannot assign a user other than yourself a class role.")
            return
        elif user != ctx.author and await has_any_role_check(ctx, *MOD_ROLES):
            log.info(
                f"Replacing {user}'s class roles at request of moderator {ctx.author}"
            )
            for role in CLASS_ROLES:
                await user.remove_roles(
                    discord.Object(role),
                    reason=f"Moderator {ctx.author} Replacing {user}'s Class Roles",
                )

        # Check if the user is self-roleing and already has a class role.
        if user == ctx.author and await has_any_role_check(ctx, *CLASS_ROLES):
            modmail = discord.utils.get(ctx.guild.members, id=575252669443211264)
            await ctx.send(
                f"You already have a class role. If you mistakenly assigned the wrong role, contact {modmail.mention}."
            )
            return

        await user.add_roles(discord.Object(CRoles.alumni), reason="Class Roles")
        log.trace(f"Assigned {user} the Alumni role")

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command(
        name="new-grade", aliases=("n-g", "ng", "new-school-year", "n-s-y", "nsy")
    )
    async def new_grade(self, ctx: commands.Context) -> None:
        """Move everyone's grade level role up one."""
        log.info(f"Started role update at the request of {ctx.author}")
        # Make role IDs into objects for easier comparison:
        freshmen = ctx.guild.get_role(CRoles.freshmen)
        sophomores = ctx.guild.get_role(CRoles.sophomores)
        juniors = ctx.guild.get_role(CRoles.juniors)
        seniors = ctx.guild.get_role(CRoles.seniors)
        alumni = ctx.guild.get_role(CRoles.alumni)
        log.trace(f"Freshmen role: {freshmen}")

        for member in ctx.guild.members:
            if freshmen in member.roles:
                await member.remove_roles(freshmen, reason="Class Roles update.")
                await member.add_roles(sophomores, reason="Class Roles update.")
                await member.send(
                    f"Your grade level role has been changed to {sophomores.name}. Have a great school year!"
                )
                log.info(f"{member} has been moved from {freshmen} to {sophomores}")
            elif sophomores in member.roles:
                await member.remove_roles(sophomores, reason="Class Roles update.")
                await member.add_roles(juniors, reason="Class Roles update.")
                await member.send(
                    f"Your grade level role has been changed to {juniors.name}. Have a great school year!"
                )
                log.info(f"{member} has been moved from {sophomores} to {juniors}")
            elif juniors in member.roles:
                await member.remove_roles(juniors, reason="Class Roles update.")
                await member.add_roles(seniors, reason="Class Roles update.")
                await member.send(
                    f"Your grade level role has been changed to {seniors.name}. Have a great school year!"
                )
                log.info(f"{member} has been moved from {juniors} to {seniors}")
            elif seniors in member.roles:
                await member.remove_roles(seniors, reason="Class Roles update.")
                await member.add_roles(alumni, reason="Class Roles update.")
                await member.send(
                    f"Your grade level role has been changed to {alumni.name}. Have fun in college!"
                )
                log.info(f"{member} has been moved from {seniors} to {alumni}")
            else:
                log.info(
                    f"{member} was either a bot or an alum, their class roles were not changed. Their roles are: {member.roles}"
                )
        await ctx.send("Updated all class roles!")


def setup(bot: commands.Bot) -> None:
    """Add the ClassRoles cog to the bot."""
    bot.add_cog(ClassRoles(bot))
