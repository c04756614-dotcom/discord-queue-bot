import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = []

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    user = ctx.author

    # prevent double-queue
    if user in queue:
        await ctx.send("You're already in queue.")
        return

    queue.append(user)
    await ctx.send(f"{user.name} joined the queue. Waiting for opponent...")

    # if 2 players, create match
    if len(queue) >= 2:
        p1 = queue.pop(0)
        p2 = queue.pop(0)

        guild = ctx.guild

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            p1: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            p2: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        channel = await guild.create_text_channel(
            name=f"match-{p1.name}-vs-{p2.name}",
            overwrites=overwrites
        )

        await channel.send(
            "🎮 MATCH FOUND!\n\n"
            f"{p1.mention} vs {p2.mention}\n\n"
            "Paste your Roblox VIP server link here."
        )

@bot.command()
async def leave(ctx):
    user = ctx.author

    if user in queue:
        queue.remove(user)
        await ctx.send("Removed from queue.")
    else:
        await ctx.send("You're not in queue.")

# TOKEN comes from Railway/Render environment variables
bot.run(os.getenv("TOKEN"))
