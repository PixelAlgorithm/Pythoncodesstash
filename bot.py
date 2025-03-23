import os
import discord
import random
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

users = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! 👋")

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"User Info - {member.name}", color=discord.Color.blue())
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else "")
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    embed = discord.Embed(title="Server Info", color=discord.Color.green())
    embed.add_field(name="Server Name", value=ctx.guild.name, inline=True)
    embed.add_field(name="Total Members", value=ctx.guild.member_count, inline=True)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Deleted {amount} messages.", delete_after=3)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member_name:
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned.")
            return
    await ctx.send("User not found in ban list.")

@bot.command()
async def mute(ctx, member: discord.Member, time: int = 60):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)

    await member.add_roles(muted_role)
    await ctx.send(f"{member.mention} has been muted for {time} seconds.")
    await asyncio.sleep(time)
    await member.remove_roles(muted_role)
    await ctx.send(f"{member.mention} is now unmuted.")

@bot.command()
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f"{member.mention} has been unmuted.")

@bot.command()
async def fun(ctx):
    responses = ["You're awesome! 😃", "Keep going! 🚀", "You got this! 💪"]
    await ctx.send(random.choice(responses))

@bot.command()
async def eightball(ctx, *, question):
    responses = ["Yes!", "No!", "Maybe...", "Definitely!", "Not a chance!"]
    await ctx.send(f"🎱 {random.choice(responses)}")

@bot.command()
async def flip(ctx):
    await ctx.send(random.choice(["Heads!", "Tails!"]))

@bot.command()
async def balance(ctx):
    user = str(ctx.author.id)
    if user not in users:
        users[user] = {"balance": 100}
    await ctx.send(f"{ctx.author.mention}, your balance is 💰 {users[user]['balance']} coins.")

@bot.command()
async def work(ctx):
    user = str(ctx.author.id)
    if user not in users:
        users[user] = {"balance": 100}
    
    earnings = random.randint(10, 50)
    users[user]["balance"] += earnings
    await ctx.send(f"{ctx.author.mention}, you worked and earned 💰 {earnings} coins! Your new balance is {users[user]['balance']}.")

@bot.command()
async def give(ctx, member: discord.Member, amount: int):
    giver = str(ctx.author.id)
    receiver = str(member.id)

    if giver not in users:
        users[giver] = {"balance": 100}
    if receiver not in users:
        users[receiver] = {"balance": 100}

    if users[giver]["balance"] >= amount and amount > 0:
        users[giver]["balance"] -= amount
        users[receiver]["balance"] += amount
        await ctx.send(f"{ctx.author.mention} gave 💰 {amount} coins to {member.mention}!")
    else:
        await ctx.send("You don't have enough coins.")

if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN not found in .env file")
