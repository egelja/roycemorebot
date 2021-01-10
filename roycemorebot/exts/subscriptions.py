import asyncio
import json
import logging
import typing
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

    # @commands.Cog.listener()
    # async def on_member_join(self, member: discord.Member) -> None:
    #     """Give every new member to the server the `DJ` role."""
    #     if not member.bot:
    #         await member.add_roles(discord.Object(StaffRoles.dj_role), reason="Auto DJ-role")

    @staticmethod
    def load_announcement_roles() -> "dict[str, dict[str, typing.Union[int, bool]]]":
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

    def reload_announcement_roles(
        self,
    ) -> "dict[str, dict[str, typing.Union[int, bool]]]":
        """Reload the list of all the announcement roles in the current guild."""
        announcement_roles = {}

        guild = discord.utils.get(self.bot.guilds, id=Guild.guild_id)
        clubs_category = discord.utils.get(guild.categories, id=Categories.clubs)

        log.trace("Starting role reload.")
        # Get server and event announcements seperately
        announcement_roles["server"] = {
            "id": discord.utils.get(guild.roles, name="Server Announcements").id,
            "club": False,
        }
        announcement_roles["event"] = {
            "id": discord.utils.get(guild.roles, name="Event Announcements").id,
            "club": False,
        }

        for channel in clubs_category.channels:
            announcement_role = discord.utils.find(
                lambda role: "Announcements" in role.name
                and role.name.lower().startswith(channel.name)
                and role.name.index(" ") == len(channel.name),  # prevents overlap
                guild.roles,
            )
            log.trace(f"Channel: {channel.name}, role: {announcement_role}")
            announcement_roles[channel.name] = {
                "id": announcement_role.id,
                "club": "club" in announcement_role.name.lower(),
            }

        log.trace("Saving announcement roles.")
        save_file = Path("data", "announcement_roles.json")
        save_file.parent.mkdir(exist_ok=True)
        with save_file.open("w") as f:
            json.dump(announcement_roles, f, indent=4)

        log.info("Announcement role reload finished")
        return announcement_roles

    @commands.guild_only()
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
            role = discord.utils.get(
                ctx.guild.roles, id=self._announcement_roles[match_info[0]]["id"]
            )
            log.trace(f"Matched role `{role}` with probability {match_info[1]}")
            await ctx.author.add_roles(
                role,
                reason="User announcements subscription",
            )
            log.info(f"User {ctx.author} subscribed to {role}")

            if ctx.message.channel.id == Channels.roles:
                await ctx.send(
                    f"{ctx.author.mention}, you have successfully subscribed to {role}.",
                    delete_after=5.0,
                )
                await asyncio.sleep(5.0)
                await ctx.message.delete()
            else:
                await ctx.send(
                    f"{ctx.author.mention}, you have successfully subscribed to {role}.",
                )
        else:
            if ctx.message.channel.id == Channels.roles:
                await ctx.send(
                    f"{ctx.author.mention}, there are no announcement roles with that name.",
                    delete_after=5.0,
                )
                await asyncio.sleep(5.0)
                await ctx.message.delete()
            else:
                await ctx.send(
                    f"{ctx.author.mention}, there are no announcement roles with that name."
                )

    @commands.guild_only()
    @commands.command(aliases=("unsub",))
    async def unsubscribe(self, ctx: commands.Context, announcement_name: str) -> None:
        """Unsubscribe to an announcement role on the server."""
        all_roles = list(self._announcement_roles.keys())
        log.trace(f"All roles: {all_roles}")
        match_info = process.extractOne(
            announcement_name,
            all_roles,
            score_cutoff=75,
        )
        log.trace(f"Match info: {match_info}")
        if match_info:
            role = discord.utils.get(
                ctx.guild.roles, id=self._announcement_roles[match_info[0]]["id"]
            )
            log.trace(f"Matched role `{role}` with probability {match_info[1]}")
            await ctx.author.remove_roles(
                role,
                reason="User announcements unsubscription",
            )
            log.info(f"User {ctx.author} unsubscribed from {role}")

            if ctx.message.channel.id == Channels.roles:
                await ctx.send(
                    f"{ctx.author.mention}, you have successfully unsubscribed from {role}.",
                    delete_after=5.0,
                )
                await asyncio.sleep(5.0)
                await ctx.message.delete()
            else:
                await ctx.send(
                    f"{ctx.author.mention}, you have successfully unsubscribed from {role}.",
                )
        else:
            if ctx.message.channel.id == Channels.roles:
                await ctx.send(
                    f"{ctx.author.mention}, there are no announcement roles with that name.",
                    delete_after=5.0,
                )
                await asyncio.sleep(5.0)
                await ctx.message.delete()
            else:
                await ctx.send(
                    f"{ctx.author.mention}, there are no announcement roles with that name."
                )

    @commands.guild_only()
    @commands.group(
        name="subscriptions", aliases=("subs",), invoke_without_command=True
    )
    async def subscriptions_group(self, ctx: commands.Context) -> None:
        """Commands group for managing announcement subscriptions."""
        await ctx.send_help(ctx.command)

    @commands.guild_only()
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
                name=f"{subscription.title()}{' Club' if self._announcement_roles[subscription]['club'] else ''} Announcements",
                value=f"`?subscribe {subscription}`",
                inline=True,
            )

        if ctx.channel.id == Channels.roles:
            await ctx.send(
                f"{ctx.author.mention}, please use a bot channel to run that command.",
                delete_after=5.0
            )
            await asyncio.sleep(5.0)
            await ctx.message.delete()
        else:
            await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.has_any_role(*MOD_ROLES)
    @subscriptions_group.command(aliases=("r",))
    async def reload(self, ctx: commands.Context) -> None:
        """Reload the announcement roles save."""
        self._announcement_roles = self.reload_announcement_roles()
        await ctx.send(f"{Emoji.ok} Successfully reloaded announcement roles!")

    @commands.guild_only()
    @commands.has_role(StaffRoles.admin_role)
    @subscriptions_group.command(name="add-club", aliases=("add", "ac", "a-c", "a"))
    async def add_club(
        self,
        ctx: commands.Context,
        channel_name: str,
        leaders: commands.Greedy[discord.Member] = None,
        club: bool = True,
        *,
        leader_title: typing.Optional[str] = "Leader",
    ) -> None:
        """Create a new club channel with corresponding roles and leaders (if given)."""
        guild = ctx.guild
        name = channel_name.replace(" ", "-").lower()  # Discord-safe channel names
        log.info(f"Creating a new club channel at the request of {ctx.author}")
        leader_names = (
            list(map(lambda l: l.name + "#" + l.discriminator, leaders))
            if leaders
            else None
        )
        log.info(
            f"Name: {name}, leaders: {leader_names}, club: {club}, leader title: {leader_title}"
        )

        # Create the roles and assign them
        leader_role = await guild.create_role(
            name=f"{name.title()}{' Club' if club else ''} {leader_title}",
            mentionable=True,
            reason="Club creation",
        )
        ann_role = await guild.create_role(
            name=f"{name.title()}{' Club' if club else ''} Announcements",
            mentionable=True,
            reason="Club creation",
        )
        log.trace(f"Created {leader_role} and {ann_role} role")

        if leaders:
            for leader in leaders:
                await leader.add_roles(leader_role, reason="Club creation")
        log.trace("Assigned leaders their roles")

        # Create the channel
        clubs_category = discord.utils.get(guild.categories, id=Categories.clubs)
        channel = await clubs_category.create_text_channel(
            name,
            overwrites={
                discord.utils.get(
                    guild.roles, id=StaffRoles.mod_role
                ): discord.PermissionOverwrite(view_channel=True, send_messages=True),
                discord.utils.get(
                    guild.roles, id=StaffRoles.muted_role
                ): discord.PermissionOverwrite(send_messages=False),
                leader_role: discord.PermissionOverwrite(
                    view_channel=True,
                    manage_channels=True,
                    manage_permissions=True,
                    send_messages=True,
                    manage_messages=True,
                ),
            },
            reason="Club creation",
        )
        position = sorted(
            clubs_category.text_channels, key=lambda channel: channel.name
        ).index(channel)
        log.trace(f"Channel index: {position}")
        await channel.edit(position=position, reason="Club creation")
        log.trace(f"Created channel {channel} and moved to postition {position}")

        # Load new announcement roles
        log.info(
            f"Reloading announcement roles because of new announcement channel {channel_name}"
        )
        self._announcement_roles = self.reload_announcement_roles()

        # Completion message
        await ctx.send(f"{Emoji.ok} Successfully added club channel!")

    @commands.guild_only()
    @commands.has_role(StaffRoles.admin_role)
    @subscriptions_group.command(
        name="remove-club", aliases=("remove", "rm-c", "rmc", "rm")
    )
    async def remove_club(
        self, ctx: commands.Context, club_channel: discord.TextChannel
    ) -> None:
        """Delete a club channel and roles."""
        log.info(
            f"Deleteing club channel {club_channel} and roles at the request of {ctx.author}"
        )
        ann_role = discord.utils.get(
            ctx.guild.roles, id=self._announcement_roles[club_channel.name]["id"]
        )
        await ann_role.delete(reason="Removing club from server")
        log.trace("Deleted announcement role")
        leader_role = discord.utils.find(
            lambda role: role.name.lower().startswith(club_channel.name),
            ctx.guild.roles,
        )
        await leader_role.delete(reason="Removing club from server")
        log.trace("Deleted leader role")
        await club_channel.delete(reason="Removing club from server")
        log.trace("Deleted channel")

        self._announcement_roles = self.reload_announcement_roles()

        # Completion message
        await ctx.send(f"{Emoji.ok} Successfully removed club channel!")


def setup(bot: commands.Bot) -> None:
    """Add the Subscriptions cog to the bot."""
    bot.add_cog(Subscriptions(bot))
