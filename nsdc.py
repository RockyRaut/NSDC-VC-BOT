import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"🇳🇵 NEPALSOCIALDC VC Bot is online as {bot.user}")

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

bot.run("MTM5MjEwNjAwNjc3NDgxMjY5Mg.GrHCkA.y8oRhANjFquVhIj1hA3_-8cy0MTucsOmhfndNk")

DISCORD_TOKEN = MTM5MjEwNjAwNjc3NDgxMjY5Mg.GrHCkA.y8oRhANjFquVhIj1hA3_-8cy0MTucsOmhfndNk
