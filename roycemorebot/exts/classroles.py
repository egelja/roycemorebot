import asyncio
import logging
import textwrap

import discord
from discord.ext import commands

from roycemorebot.checks import has_any_role_check, has_no_roles_check
from roycemorebot.constants import CLASS_ROLES, Channels, MOD_ROLES
from roycemorebot.constants import ClassRoles as CRoles
from roycemorebot.constants import Emoji, Guild, Messages

log = logging.getLogger(__name__)

WELCOME_MESSAGE = textwrap.dedent(
    f"""\
    **__To get started:__**
    - Read the rules if you didn't already.

    - **Go to the [#roles]({Messages.roles}) channel** and get a Class Role.
    *Note: __This is mandatory!__ Read Rule #6.*

    - Server invite link is {Guild.invite_link}. Invite your friends!

    All of this, and more, is described in [#welcome]({Messages.welcome}).
    """
)


class ClassRoles(commands.Cog, name="Class Roles"):
    """User-assigned roles based on their grade."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, old: discord.Member, new: discord.Member) -> None:
        """Send a welcome message to new members of the server."""
        if old.pending and not new.pending:
            # Someone has just verified, send them a welcome message!
            embed = discord.Embed(
                color=discord.Colour.green(),
                description=WELCOME_MESSAGE,
            ).set_author(
                name="Welcome to the Roycemore Discord Server!",
                icon_url=new.guild.icon_url,
            )

            log.trace(new.guild.icon_url)
            log.info(f"Member {new} has just verified, sending them a welcome message!")

            await new.send(embed=embed)

    async def _send_but_delete_in_roles(
        self, ctx: commands.Context, message: str
    ) -> None:
        """Send a message, but if it's in #roles, delete it after 5 seconds."""
        if ctx.message.channel.id == Channels.roles:
            await ctx.send(message, delete_after=5.0)
            await asyncio.sleep(5.0)
            await ctx.message.delete()
        else:
            await ctx.send(message)

    async def _add_class_role(
        self, ctx: commands.Context, user: discord.Member, role: int, role_name: str
    ) -> None:
        """Give a user a class role."""
        # Default to the user being the author
        if user is None:
            user = ctx.author
        # Check if the user is not a mod and they tried to give someone else a role.
        if user != ctx.author and await has_no_roles_check(ctx, *MOD_ROLES):
            await self._send_but_delete_in_roles(
                ctx,
                f"{Emoji.no} You cannot assign a user other than yourself a class "
                + "role.",
            )
            return
        elif user != ctx.author and await has_any_role_check(ctx, *MOD_ROLES):
            log.info(
                f"Replacing {user}'s class roles at request of moderator {ctx.author}"
            )
            for old_role in CLASS_ROLES:
                await user.remove_roles(
                    discord.Object(old_role),
                    reason=f"Moderator {ctx.author} replacing {user}'s Class Roles",
                )
            await user.add_roles(discord.Object(role), reason="Class Roles")
            log.trace(f"Assigned {user} the {role_name} role")
            await self._send_but_delete_in_roles(
                f"{Emoji.ok} User `{user}` has been given the {role_name} role."
            )
            return

        # Check if the user is self-roleing and already has a class role.
        if user == ctx.author and await has_any_role_check(ctx, *CLASS_ROLES):
            modmail = discord.utils.get(ctx.guild.members, id=575252669443211264)
            await self._send_but_delete_in_roles(
                ctx,
                f"{Emoji.no} You already have a class role. If you mistakenly "
                + f"assigned the wrong role, contact {modmail.mention}.",
            )
            return

        await user.add_roles(discord.Object(role), reason="Class Roles")
        log.info(f"Assigned {user} the {role_name} role")

        await self._send_but_delete_in_roles(
            ctx,
            f"{ctx.author.mention}, you have successfully been given the "
            + f"{role_name} role.",
        )

    async def _update_class_role(
        self, user: discord.Member, old_role: discord.Role, new_role: discord.Role
    ) -> None:
        """Move a class role up one."""
        await user.remove_roles(old_role, reason="Class Roles update.")
        await user.add_roles(new_role, reason="Class Roles update.")
        # await user.send(
        #     f"Your grade level role has been changed to {new_role.name}. "
        #     + "Have a great school year!"
        # )
        log.trace(f"{user} has been moved from {old_role} to {new_role}")

    @commands.guild_only()
    @commands.command(name="5th-grade", aliases=("5th", "5th-grader"))
    async def grade_5(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a 5th Grader the `5th Graders` role."""
        await self._add_class_role(ctx, user, CRoles.grade_5, "5th Graders")

    @commands.guild_only()
    @commands.command(name="6th-grade", aliases=("6th", "6th-grader"))
    async def grade_6(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a 6th Grader the `6th Graders` role."""
        await self._add_class_role(ctx, user, CRoles.grade_6, "6th Graders")

    @commands.guild_only()
    @commands.command(name="7th-grade", aliases=("7th", "7th-grader"))
    async def grade_7(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a 7th Grader the `7th Graders` role."""
        await self._add_class_role(ctx, user, CRoles.grade_7, "7th Graders")

    @commands.guild_only()
    @commands.command(name="8th-grade", aliases=("8th", "8th-grader"))
    async def grade_8(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give an 8th Grader the `8th Graders` role."""
        await self._add_class_role(ctx, user, CRoles.grade_8, "8th Graders")

    @commands.guild_only()
    @commands.command(aliases=("fm", "freshmen"))
    async def freshman(
        self, ctx: commands.Context, user: discord.Member = None
    ) -> None:
        """Give a freshman the `Freshmen` role."""
        await self._add_class_role(ctx, user, CRoles.freshmen, "Freshmen")

    @commands.guild_only()
    @commands.command(aliases=("sm", "sophomores"))
    async def sophomore(
        self, ctx: commands.Context, user: discord.Member = None
    ) -> None:
        """Give a sophomore the `Sophomore` role."""
        self._add_class_role(ctx, user, CRoles.sophomores, "Sophomores")

    @commands.guild_only()
    @commands.command(aliases=("jr", "juniors"))
    async def junior(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a junior the `Junior` role."""
        self._add_class_role(ctx, user, CRoles.juniors, "Juniors")

    @commands.guild_only()
    @commands.command(aliases=("sr", "seniors"))
    async def senior(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a senior the `Senior` role."""
        self._add_class_role(ctx, user, CRoles.seniors, "Seniors")

    @commands.guild_only()
    @commands.command(aliases=("al", "alumni"))
    async def alum(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Give a alum the `Alumni` role."""
        self._add_class_role(ctx, user, CRoles.alumni, "Alumni")

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command(name="new-grade", aliases=("ng", "new-school-year"))
    async def new_grade(self, ctx: commands.Context) -> None:
        """Move everyone's grade level role up one."""
        log.info(f"Started role update at the request of {ctx.author}")
        # Make role IDs into objects for easier comparison:
        grade_5 = ctx.guild.get_role(CRoles.grade_5)
        grade_6 = ctx.guild.get_role(CRoles.grade_6)
        grade_7 = ctx.guild.get_role(CRoles.grade_7)
        grade_8 = ctx.guild.get_role(CRoles.grade_8)

        freshmen = ctx.guild.get_role(CRoles.freshmen)
        sophomores = ctx.guild.get_role(CRoles.sophomores)
        juniors = ctx.guild.get_role(CRoles.juniors)
        seniors = ctx.guild.get_role(CRoles.seniors)
        alumni = ctx.guild.get_role(CRoles.alumni)
        log.trace(f"Freshmen role: {freshmen}")

        for member in ctx.guild.members:
            if grade_5 in member.roles:
                await self._update_class_role(member, grade_5, grade_6)
            elif grade_6 in member.roles:
                await self._update_class_role(member, grade_6, grade_7)
            elif grade_7 in member.roles:
                await self._update_class_role(member, grade_7, grade_8)
            elif grade_8 in member.roles:
                await self._update_class_role(member, grade_8, freshmen)
            elif freshmen in member.roles:
                await self._update_class_role(member, freshmen, sophomores)
            elif sophomores in member.roles:
                await self._update_class_role(member, sophomores, juniors)
            elif juniors in member.roles:
                await self._update_class_role(member, juniors, seniors)
            elif seniors in member.roles:
                await member.remove_roles(seniors, reason="Class Roles update.")
                await member.add_roles(alumni, reason="Class Roles update.")
                # await member.send(
                #     f"Your grade level role has been changed to {alumni.name}. "
                #     + "Have fun in college!"
                # )
                log.trace(f"{member} has been moved from {seniors} to {alumni}")
            else:
                log.trace(
                    f"{member} was either a bot or an alum, their class roles were "
                    + f"not changed. Their roles are: {member.roles}"
                )
        log.info("Class roles update finished")
        await ctx.send("Updated all class roles!")


def setup(bot: commands.Bot) -> None:
    """Add the ClassRoles cog to the bot."""
    bot.add_cog(ClassRoles(bot))
