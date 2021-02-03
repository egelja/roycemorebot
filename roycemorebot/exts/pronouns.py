import asyncio
import logging

import discord
from discord.ext import commands

from roycemorebot.checks import has_any_role_check
from roycemorebot.constants import Channels, PronounRoles

log = logging.getLogger(__name__)


class Pronouns(commands.Cog, name="Pronoun Roles"):
    """User-assigned roles based on their pronouns."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="he-him", aliases=("he", "him", "hehim"))
    async def he_him(self, ctx: commands.Context) -> None:
        """Toggle the `He/Him` Role."""
        if await has_any_role_check(ctx, PronounRoles.he_him):
            await ctx.author.remove_roles(
                discord.Object(PronounRoles.he_him),
                reason="Pronoun Roles",
            )
        else:
            await ctx.author.add_roles(
                discord.Object(PronounRoles.he_him), reason="Pronoun Roles"
            )
        log.info(f"Toggled {ctx.author}'s He/Him role")

        if ctx.message.channel.id == Channels.roles:
            await ctx.send(
                f"{ctx.author.mention}, you have successfully toggled the He/Him "
                + "role.",
                delete_after=5.0,
            )
            await asyncio.sleep(5.0)
            await ctx.message.delete()
        else:
            await ctx.send(
                f"{ctx.author.mention}, you have successfully toggled the He/Him "
                + "role.",
            )

    @commands.guild_only()
    @commands.command(name="she-her", aliases=("she", "her", "sheher"))
    async def she_her(self, ctx: commands.Context) -> None:
        """Toggle the `She/Her` Role."""
        if await has_any_role_check(ctx, PronounRoles.she_her):
            await ctx.author.remove_roles(
                discord.Object(PronounRoles.she_her),
                reason="Pronoun Roles",
            )
        else:
            await ctx.author.add_roles(
                discord.Object(PronounRoles.she_her), reason="Pronoun Roles"
            )
        log.info(f"Toggled {ctx.author}'s She/Her role")

        if ctx.message.channel.id == Channels.roles:
            await ctx.send(
                f"{ctx.author.mention}, you have successfully toggled the She/Her "
                + "role.",
                delete_after=5.0,
            )
            await asyncio.sleep(5.0)
            await ctx.message.delete()
        else:
            await ctx.send(
                f"{ctx.author.mention}, you have successfully toggled the She/Her "
                + "role.",
            )

    @commands.guild_only()
    @commands.command(name="they-them", aliases=("they", "them", "theythem"))
    async def they_them(self, ctx: commands.Context) -> None:
        """Toggle the `They/Them` Role."""
        if await has_any_role_check(ctx, PronounRoles.they_them):
            await ctx.author.remove_roles(
                discord.Object(PronounRoles.they_them),
                reason="Pronoun Roles",
            )
        else:
            await ctx.author.add_roles(
                discord.Object(PronounRoles.they_them), reason="Pronoun Roles"
            )
        log.info(f"Toggled {ctx.author}'s They/Them role")

        if ctx.message.channel.id == Channels.roles:
            await ctx.send(
                f"{ctx.author.mention}, you have successfully toggled the They/Them "
                + "role.",
                delete_after=5.0,
            )
            await asyncio.sleep(5.0)
            await ctx.message.delete()
        else:
            await ctx.send(
                f"{ctx.author.mention}, you have successfully toggled the They/Them "
                + "role.",
            )


def setup(bot: commands.Bot) -> None:
    """Add the Pronouns cog to the bot."""
    bot.add_cog(Pronouns(bot))
