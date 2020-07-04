# Okay, here i go. This is the bot i made for the competition. If you don't already know,
# it's an arcade bot. It has multiple features such as Connect Four, tic-tac-toe, a candy game
# and much more. Tic-Tac-Toe is in JS, i don't really know JS and i can't be asked to learn
# so i just found a module for tic-tac-toe and used that. pls excuse that :3. also,
# i commented on these as fast as i could so please excuse any spelling mistakes
# or very, very light explanations, sometimes even none.
# well, lets get started!

import discord
import config

from discord.ext import commands


# I figured Auto-Sharding it would be good, although i don't need it until it's in at least 2k servers.
class ArcadeBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("arc!"))


bot = ArcadeBot()

# Here, we will load the bots cogs and set its status to `Playing Arcade Games`.
@bot.event
async def on_ready():
    bot.remove_command("help")
    for ext in config.initial_ext:
        bot.load_extension(ext)
    print("Bot started.")
    print(f"Cogs Loaded: {len(bot.cogs)}")
    print(f"shards: {len(bot.shards)}")
    await bot.change_presence(activity=discord.Game(name="Arcade Games"))

# Basic shutdown command.
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Goodbye.")
    await bot.logout()

# Ping command.
@bot.command()
async def ping(ctx):
    await ctx.send(f"**Pong!** :ping_pong:\nBot Latency: {round(bot.latency*1000)}ms")

# Run the bot.
bot.run(config.token)
