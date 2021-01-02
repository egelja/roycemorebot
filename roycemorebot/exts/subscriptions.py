import asyncio
import json
import logging
from pathlib import Path

import discord
from discord.ext import commands

from roycemorebot.constants import Categories, Channels, Guild, StaffRoles

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
                await mod_bot_channel.send("Announcement roles reloaded!")
            else:
                log.info(f"Announcement role reload canceled by {user}")
                await mod_bot_channel.send(
                    "Announcement role reload canceled. Use `?subscriptions reload` to reload the announcement roles."
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
                and channel.name in role.name.lower(),
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


def setup(bot: commands.Bot) -> None:
    """Add the Subscriptions cog to the bot."""
    bot.add_cog(Subscriptions(bot))
