import asyncio
import json
import logging
from pathlib import Path

import discord
from discord.ext import commands
from fuzzywuzzy import process

from roycemorebot.constants import (
    MOD_ROLES,
    Categories,
    Channels,
    Emoji,
    Guild,
    StaffRoles,
)

log = logging.getLogger(__name__)


class Subscriptions(commands.Cog):
    """User-assigned subscriptions to select announcements."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._announcement_roles = self.load_announcement_roles()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Load the announcement roles, but only once guilds are available."""
        if self._announcement_roles != {}:
            return

        log.info("No announcement roles found, requesting to reload")
        mod_bot_channel = self.bot.get_channel(Channels.mod_bot_commands)
        guild = discord.utils.get(self.bot.guilds, id=Guild.guild_id)
        mod_role = discord.utils.get(guild.roles, id=StaffRoles.mod_role)
        msg = await mod_bot_channel.send(
            f"{mod_role.mention}\nNo announcement roles are loaded. Reload?"
        )

        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add",
                timeout=300.0,
                check=lambda r, u: str(r.emoji) in ["✅", "❌"]
                and r.message == msg
                and not u.bot,
            )
        except asyncio.TimeoutError:
            log.info("Reload timed out")
            await mod_bot_channel.send(
                "Announcement role reload timeout. Use `?subscriptions reload` to reload the announcement roles."
            )
        else:
            if str(reaction.emoji) == "✅":
                log.info(f"Announcement role reload started by {user}")
                self._announcement_roles = self.reload_announcement_roles()
                await mod_bot_channel.send(
                    f"{Emoji.ok} Successfully reloaded announcement roles!"
                )
            else:
                log.info(f"Announcement role reload canceled by {user}")
                await mod_bot_channel.send(
                    f"{Emoji.no} Announcement role reload canceled. Use `?subscriptions reload` to reload the announcement roles."
                )

    @staticmethod
    def load_announcement_roles() -> "dict[str, int]":
        """Load all the announcement roles from the save file."""
        save_file = Path("data", "announcement_roles.json")

        if save_file.is_file():
            log.info("Loaded announcement roles from save file")
            with save_file.open("r") as f:
                roles = json.load(f)
                log.trace(f"File contents: {roles}")
                return roles
        else:
            return {}  # Checked later in `on_ready` and loaded from guild.

    def reload_announcement_roles(self) -> "dict[str, int]":
        """Reload the list of all the announcement roles in the current guild."""
        announcement_roles = {}

        guild = discord.utils.get(self.bot.guilds, id=Guild.guild_id)
        clubs_category = discord.utils.get(guild.categories, id=Categories.clubs)

        log.trace("Starting role reload.")
        # Get server and event announcements seperately
        announcement_roles["server"] = discord.utils.get(
            guild.roles, name="Server Announcements"
        )
        announcement_roles["event"] = discord.utils.get(
            guild.roles, name="Event Announcements"
        )

        for channel in clubs_category.channels:
            announcement_role = discord.utils.find(
                lambda role: "Announcements" in role.name
                and role.name.lower().startswith(channel.name),
                guild.roles,
            )
            announcement_roles[channel.name] = announcement_role.id
            log.trace(f"Channel: {channel.name}, role: {announcement_role}")

        log.trace("Saving announcement roles.")
        save_file = Path("data", "announcement_roles.json")
        save_file.parent.mkdir(exist_ok=True)
        with save_file.open("w") as f:
            json.dump(announcement_roles, f, indent=4)

        log.info("Announcement role reload finished")
        return announcement_roles

    @commands.command(aliases=("sub",))
    async def subscribe(self, ctx: commands.Context, announcement_name: str) -> None:
        """Subscribe to an announcement role on the server."""
        all_roles = list(self._announcement_roles.keys())
        log.trace(f"All roles: {all_roles}")
        match_info = process.extractOne(
            announcement_name,
            all_roles,
            score_cutoff=75,
        )
        log.trace(f"Match info: {match_info}")
        if match_info:
            role_name = match_info[0]
            log.trace(f"Matched role `{role_name}` with probability {match_info[1]}")
            await ctx.author.add_roles(
                discord.Object(self._announcement_roles[role_name]),
                reason="User announcements subscription",
            )
            log.info(f"User {ctx.author} subscribed to {role_name}")
            await ctx.send(
                f"{ctx.author.mention}, you have successfully subscribed to {role_name} Announcements."
            )
        else:
            await ctx.send(
                f"{ctx.author.mention}, there are no announcement roles with that name."
            )

    @commands.group(
        name="subscriptions", aliases=("subs",), invoke_without_command=True
    )
    async def subscriptions_group(self, ctx: commands.Context) -> None:
        """Commands group for managing announcement subscriptions."""
        await ctx.send_help(ctx.command)

    @subscriptions_group.command(name="list", aliases=("l", "ls"))
    async def list_subscriptions(self, ctx: commands.Context) -> None:
        """List all possible announcement subscriptions and their corresponding commands."""
        embed = discord.Embed(
            title="Announcement Subscriptions",
            description="Here are all the possible announcement subscriptions and their commands.",
            color=discord.Colour.green(),
        )

        all_subs = list(self._announcement_roles.keys())
        for subscription in all_subs:
            embed.add_field(
                name=f"{subscription.title()} Announcements",
                value=f"`?subscribe {subscription}`",
                inline=True,
            )

        await ctx.send(embed=embed)

    @commands.has_any_role(*MOD_ROLES)
    @subscriptions_group.command(aliases=("r",))
    async def reload(self, ctx: commands.Context) -> None:
        """Reload the announcement roles save."""
        self._announcement_roles = self.reload_announcement_roles()
        await ctx.send(f"{Emoji.ok} Successfully reloaded announcement roles!")


def setup(bot: commands.Bot) -> None:
    """Add the Subscriptions cog to the bot."""
    bot.add_cog(Subscriptions(bot))
