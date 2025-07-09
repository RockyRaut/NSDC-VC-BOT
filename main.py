import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event to sync slash commands
@bot.event
async def on_ready():
    await bot.wait_until_ready()
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced! {len(synced)} commands registered.")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    print(f"🇳🇵 NEPALSOCIALDC VC Bot is online as {bot.user}")

@bot.tree.command(name="vc-lock", description="Locks your current voice channel")
async def vc_lock(interaction: discord.Interaction):
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("❌ You must be in a voice channel!", ephemeral=True)
        return

    channel = interaction.user.voice.channel

    try:
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.connect = False
        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message(f"🔒 Locked VC: **{channel.name}**")
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Error: {e}", ephemeral=True)

@bot.tree.command(name="vc_unlock", description="Unlocks your current voice channel")
async def vc_unlock(interaction: discord.Interaction):
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("❌ You must be in a voice channel!", ephemeral=True)
        return
    
    channel = interaction.user.voice.channel

    try:
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.connect = None  # Removes the overwrite, unlocking
        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message(f"🔓 Unlocked VC: **{channel.name}**")
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Error: {e}", ephemeral=True)


@bot.tree.command(name="vc_set_user", description="Allow a user to connect to your voice channel")
@app_commands.describe(user="User to allow to connect")
async def vc_set_user(interaction: discord.Interaction, user: discord.Member):
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("❌ You must be in a voice channel!", ephemeral=True)
        return

    channel = interaction.user.voice.channel

    try:
        overwrite = channel.overwrites_for(user)
        overwrite.connect = True
        await channel.set_permissions(user, overwrite=overwrite)
        await interaction.response.send_message(f"✅ Allowed {user.mention} to connect to **{channel.name}**")
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Error: {e}", ephemeral=True)


@bot.tree.command(name="vc_kick_members", description="Kick all members from your voice channel except yourself")
async def vc_kick_members(interaction: discord.Interaction):
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("❌ You must be in a voice channel!", ephemeral=True)
        return

    channel = interaction.user.voice.channel
    members = channel.members

    try:
        kicked = []
        for member in members:
            if member != interaction.user:
                await member.move_to(None)  # Disconnect member
                kicked.append(member.display_name)
        await interaction.response.send_message(f"👢 Kicked members: {', '.join(kicked)}")
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Error: {e}", ephemeral=True)


@bot.tree.command(name="vc_invite_member", description="Invite a user to your voice channel (allow connect)")
@app_commands.describe(user="User to invite")
async def vc_invite_member(interaction: discord.Interaction, user: discord.Member):
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("❌ You must be in a voice channel!", ephemeral=True)
        return

    channel = interaction.user.voice.channel

    try:
        overwrite = channel.overwrites_for(user)
        overwrite.connect = True
        await channel.set_permissions(user, overwrite=overwrite)
        await interaction.response.send_message(f"📨 Invited {user.mention} to **{channel.name}**")
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Error: {e}", ephemeral=True)

@bot.command()
async def vc_lock(ctx, role: discord.Role = None):
    """Lock the current VC to a role or just yourself."""
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.set_permissions(ctx.guild.default_role, connect=False)

        if role:
            await channel.set_permissions(role, connect=True)
            await ctx.send(f"🔒 VC **{channel.name}** locked for role: `{role.name}`.")
        else:
            await channel.set_permissions(ctx.author, connect=True)
            await ctx.send(f"🔒 VC **{channel.name}** locked for you only.")
    else:
        await ctx.send("❌ You need to be in a VC to use this.")

@bot.command()
async def vc_unlock(ctx):
    """Unlock the VC for everyone."""
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.set_permissions(ctx.guild.default_role, connect=True)
        await ctx.send(f"🔓 VC **{channel.name}** is now open to all.")
    else:
        await ctx.send("❌ You must be in a VC to unlock it.")

@bot.command()
async def vc_invite(ctx, member: discord.Member):
    """Invite someone to your locked VC."""
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.set_permissions(member, connect=True)
        await ctx.send(f"✅ Invited {member.mention} to **{channel.name}**.")
    else:
        await ctx.send("❌ You must be in a VC to invite someone.")

@bot.command()
async def vc_kick(ctx, member: discord.Member):
    """Kick someone from your current VC."""
    if ctx.author.voice and ctx.author.voice.channel:
        vc = ctx.author.voice.channel
        if member in vc.members:
            await member.move_to(None)
            await ctx.send(f"👢 Kicked `{member.display_name}` from **{vc.name}**.")
        else:
            await ctx.send("❌ That user is not in your VC.")
    else:
        await ctx.send("❌ You must be in a VC to kick someone.")
import os
bot.run(os.getenv("DISCORD_TOKEN"))
