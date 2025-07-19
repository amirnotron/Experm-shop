import discord
import asyncio
import os
from datetime import timezone, timedelta , datetime
from discord.ext import commands , tasks
from discord import app_commands
from discord import ui, Embed , File

class MyCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Ban a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member == interaction.guild.owner:
            await interaction.response.send_message("You cannot ban the server owner!", ephemeral=True)
            return

        if member == self.bot.user:
            await interaction.response.send_message("I cannot ban myself!", ephemeral=True)
            return

        if member == interaction.user:
            await interaction.response.send_message("You cannot ban yourself!", ephemeral=True)
            return

        if interaction.guild.me.top_role <= member.top_role:
            await interaction.response.send_message(f"I cannot ban {member.mention} as their role is equal to or higher than my highest role.", ephemeral=True)
            return

        if interaction.user.top_role <= member.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message(f"You cannot ban {member.mention} as their role is equal to or higher than your highest role.", ephemeral=True)
            return

        try:
            await member.ban(reason=reason)
            embed = Embed(
                title="Member Banned",
                description=f"{member.mention} has been banned.",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason if reason else "No reason provided.")
            embed.set_footer(text=f"Banned by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have sufficient permissions to ban this member. Make sure my role is above theirs.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred while trying to ban {member.mention}: {e}", ephemeral=True)

    @app_commands.command(name="clear", description="Clear a specified number of messages from the channel.")
    @app_commands.describe(amount="The number of messages to delete (1-100).")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 500]):

        await interaction.response.defer(ephemeral=True)

        try:
            deleted = await interaction.channel.purge(limit=amount)
            embed = Embed(
                title="Messages Cleared",
                description=f"Successfully deleted {len(deleted)} messages from {interaction.channel.mention}.",
                color=discord.Color.dark_blue()
            )
            embed.set_footer(text=f"Cleared by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("I do not have sufficient permissions to delete messages in this channel. Make sure I have 'Manage Messages'.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An unexpected error occurred while trying to clear messages: {e}", ephemeral=True)

    @app_commands.command(name="kick", description="Kick a member from the server.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):

        if member == interaction.guild.owner:
            await interaction.response.send_message("You cannot kick the server owner!", ephemeral=True)
            return

        if member == self.bot.user:
            await interaction.response.send_message("I cannot kick myself!", ephemeral=True)
            return

        if member == interaction.user:
            await interaction.response.send_message("You cannot kick yourself!", ephemeral=True)
            return

        if interaction.guild.me.top_role <= member.top_role:
            await interaction.response.send_message(f"I cannot kick {member.mention} as their role is equal to or higher than my highest role.", ephemeral=True)
            return
 
        if interaction.user.top_role <= member.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message(f"You cannot kick {member.mention} as their role is equal to or higher than your highest role.", ephemeral=True)
            return

        try:
            await member.kick(reason=reason)
            embed = Embed(
                title="Member Kicked",
                description=f"{member.mention} has been kicked.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Reason", value=reason if reason else "No reason provided.")
            embed.set_footer(text=f"Kicked by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have sufficient permissions to kick this member. Make sure my role is above theirs.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred while trying to kick {member.mention}: {e}", ephemeral=True)

    @app_commands.command(name="timeout", description="Timeout a member for a specified duration.")
    @app_commands.describe(
        member="The member to timeout.",
        duration_minutes="Duration in minutes (max 28 days = 40320 minutes).",
        reason="Reason for the timeout."
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration_minutes: app_commands.Range[int, 1, 40320], reason: str = None):

        if member == interaction.guild.owner:
            await interaction.response.send_message("You cannot timeout the server owner!", ephemeral=True)
            return

        if member == self.bot.user:
            await interaction.response.send_message("I cannot timeout myself!", ephemeral=True)
            return

        if member == interaction.user:
            await interaction.response.send_message("You cannot timeout yourself!", ephemeral=True)
            return

        if interaction.guild.me.top_role <= member.top_role:
            await interaction.response.send_message(f"I cannot timeout {member.mention} as their role is equal to or higher than my highest role.", ephemeral=True)
            return

        if interaction.user.top_role <= member.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message(f"You cannot timeout {member.mention} as their role is equal to or higher than your highest role.", ephemeral=True)
            return

        try:
            await member.timeout(timedelta(minutes=duration_minutes), reason=reason)
            embed = Embed(
                title="Member Timed Out",
                description=f"{member.mention} has been timed out for {duration_minutes} minutes.",
                color=discord.Color.gold()
            )
            embed.add_field(name="Reason", value=reason if reason else "No reason provided.")
            embed.set_footer(text=f"Timed out by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have sufficient permissions to timeout this member. Make sure my role is above theirs and I have 'Moderate Members'.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'Failed to timeout {member.mention}: {e}', ephemeral=True)

    @app_commands.command(name="join", description="Join a voice channel.")
    @app_commands.describe(channel="The voice channel to join (optional, defaults to your current channel).")
    async def join(self, interaction: discord.Interaction, channel: discord.VoiceChannel = None):

        target_channel = channel

        if target_channel is None:
            if interaction.user.voice and interaction.user.voice.channel:
                target_channel = interaction.user.voice.channel
            else:
                await interaction.response.send_message("You are not connected to a voice channel, and no channel was specified. Please join a voice channel or provide one to join.", ephemeral=True)
                return

        perms = target_channel.permissions_for(interaction.guild.me)
        if not perms.connect:
            await interaction.response.send_message(f"I don't have permission to connect to {target_channel.mention}.", ephemeral=True)
            return
        if not perms.speak:
            await interaction.response.send_message(f"I can connect to {target_channel.mention}, but I don't have permission to speak there.", ephemeral=True)
            pass

        try:
            if interaction.guild.voice_client:
                if interaction.guild.voice_client.channel == target_channel:
                    await interaction.response.send_message(f"I am already in {target_channel.mention}!", ephemeral=True)
                else:
                    await interaction.guild.voice_client.move_to(target_channel)
                    await interaction.response.send_message(f"Moved to {target_channel.mention}", ephemeral=False)
            else:
                await target_channel.connect()
                await interaction.response.send_message(f"Joined {target_channel.mention}", ephemeral=False)
        except discord.ClientException:
            await interaction.response.send_message("I am already connected to a voice channel.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred while trying to join the voice channel: {e}", ephemeral=True)

    @app_commands.command(name="userinfo", description="Show detailed information about a user.")
    @app_commands.describe(member="The member to get info about (optional, defaults to yourself).")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):

        if member is None:
            member = interaction.user

        if isinstance(member, discord.User) and interaction.guild:
            try:
                member = await interaction.guild.fetch_member(member.id)
            except discord.NotFound:
                await interaction.response.send_message("Could not find that member in this server.", ephemeral=True)
                return
            except Exception as e:
                await interaction.response.send_message(f"An error occurred fetching member data: {e}", ephemeral=True)
                return
        elif not isinstance(member, discord.Member):
            await interaction.response.send_message("This command can only show full info for members within a server.", ephemeral=True)
            return

        permissions = [
            perm[0].replace('_', ' ').title()
            for perm in member.guild_permissions
            if perm[1] and perm[0] not in ['read_messages', 'send_messages', 'read_message_history']
        ]

        embed = discord.Embed(title=f"User Info: {member.display_name}", color=discord.Color.blue())
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Username", value=member.name, inline=False)
        if member.discriminator != "0":
             embed.add_field(name="Discriminator", value=member.discriminator, inline=False)
        embed.add_field(name="Display Name", value=member.display_name, inline=False)
        embed.add_field(name="Bot?", value="Yes" if member.bot else "No", inline=False)
        embed.add_field(name="Top Role", value=member.top_role.mention if member.top_role else "None", inline=False)
        
        roles = sorted([role.mention for role in member.roles if role.name != "@everyone"], key=lambda r: member.guild.get_role(int(r.strip('<@&>'))).position, reverse=True)
        embed.add_field(name="Roles", value=", ".join(roles) if roles else "No roles", inline=False)
        
        embed.add_field(name="Account Created", value=discord.utils.format_dt(member.created_at, "F"), inline=False)
        embed.add_field(name="Joined Server", value=discord.utils.format_dt(member.joined_at, "F"), inline=False)
        
        if permissions:
            perms_str = ", ".join(permissions)
            if len(perms_str) > 1024:
                embed.add_field(name="Key Permissions", value="Too many to list here. (User has many permissions)", inline=False)
            else:
                embed.add_field(name="Key Permissions", value=perms_str, inline=False)
        else:
            embed.add_field(name="Key Permissions", value="No specific permissions beyond @everyone.", inline=False)

        embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        embed.timestamp = datetime.now()

        await interaction.response.send_message(embed=embed, ephemeral=False)

    @app_commands.command(name="kiss", description="Send a virtual kiss to someone!")
    @app_commands.describe(member="The member to kiss.")
    async def kiss(self, interaction: discord.Interaction, member: discord.Member):

        if member == interaction.user:
            await interaction.response.send_message("You can't kiss yourself! Find a friend to share the love with.", ephemeral=True)
            return
        if member == self.bot.user:
            await interaction.response.send_message("Aww, thanks for the kiss! *blushes*", ephemeral=False)
            return

        embed = discord.Embed(
            title=f"**{interaction.user.display_name} Kissed {member.display_name} ❤**",
            description=f"I think {interaction.user.mention} loves you, {member.mention}!",
            color=discord.Color.pink(),
            timestamp=datetime.now()
        )

        embed.set_image(url="https://media.tenor.com/m/b7DWF8ecBkIAAAAd/kiss-anime-anime.gif")
        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(MyCommands(bot))
    print("MyCommands cog loaded successfully.")