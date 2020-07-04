import discord

from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

import json
import asyncio

from .utils.data import BotData, isBlacklisted


class Candy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.botdata = BotData(self.bot)

    # The candy game.
    # <summary>
    #   this command is all about reaction time.
    #   the faster you react, the more chance you win.
    #   the first to react wins.
    #   they will be added 1 candy to their balance.
    # </summary>
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10.0, BucketType.user)
    @isBlacklisted()
    async def candy(self, ctx):
        pembed = discord.Embed(
            title="Candy",
            description="The countdown will **start soon**. **Get Ready!**",
            colour=0x2F3136,
        ) # setup the 1st embed.
        pembed.set_thumbnail(url=self.botdata.uris["candy"])
        pembed = await ctx.send(embed=pembed) # send it
        await asyncio.sleep(3)  # and wait 3 seconds to get people ready.

        await pembed.edit(
            embed=discord.Embed(
                title="Starting...", description="**Starting Now!**", colour=0x2F3136
            ).set_thumbnail(url=self.botdata.uris["candy"])
        )   # i know this may be messy, but it works xD.

        await asyncio.sleep(0.5) # wait 0.5 seconds

        for i in range(3, 0, -1):
            await pembed.edit(                                         # -----|
                embed=discord.Embed(                                   #      |
                    title=f"Countdown Phrase\n{i}", colour=0x2F3136    #      | --- Here we are counting down
                ).set_thumbnail(url=self.botdata.uris["candy"])        #      | --- from 3 to 1.
            )                                                          #      |
            await asyncio.sleep(1)                                     # -----|

        embed = discord.Embed(
            title="Candy",
            description="🍬 | First one to take the candy gets it!",
            colour=0x2F3136,
        ) # Now we get to the real thing. here we send the `game`.
        embed.set_thumbnail(url=self.botdata.uris["candy"])
        await pembed.edit(embed=embed)
        await pembed.add_reaction("🍬") # Now the reaction is added.

        def check(reaction, user):
            return (
                user != self.bot.user   # Check that the person who reacted is not the bot
                and str(reaction.emoji) == "🍬" # Check that the reaction added is the `candy` emoji.
                and reaction.message.id == pembed.id # check that the id of the message that has been reacted to
            )   # is the same as the embed id.

        msg0 = await self.bot.wait_for("reaction_add", check=check) # now add the reaction.

        # change the description to show the winner
        embed.description = f"🍬 | {msg0[1].mention} won and ate the candy!" 

        await pembed.edit(embed=embed) # send the new embed.

        # Now, let's get their balance.
        with open("db/candylb.json", "r") as f:

            l = json.load(f)

        try:

            # try incrementing their current balance by 1.
            l[str(msg0[1].id)] += 1
        except KeyError:
            
            # if their balance does not exist, we will get a `KeyError`
            # if we do, set their balance to one.
            l[str(msg0[1].id)] = 1

        with open("db/candylb.json", "w") as f:

            json.dump(l, f, indent=4)   # now save the balance.

    # The candy leaderboard.
    # <summary>
    #   this command will display the first 5 people on the candy leaderboard.
    # </summary>
    @candy.command(aliases=["lb", "top"])
    @commands.cooldown(1, 5.0, BucketType.user)
    @isBlacklisted()
    async def leaderboard(self, ctx):

        with open("db/candylb.json", "r") as f:

            l = json.load(f)    # load the leaderboard

        lb = sorted(l, key=lambda x: l[x], reverse=True) # sort the json result in order.
        res = ""

        counter = 0 # set the counter

        for a in lb: # iterate through the sorted dictionary

            counter += 1    # increment the counter

            if counter > 5: # if the counter is over 5, don't do anything.

                pass

            else:   # else, add the user to the final result.

                u = self.bot.get_user(int(a))
                res += f"\n**{counter}.** `{u}` - **{l[str(a)]} 🍬**"

        embed = discord.Embed(description=res, colour=0x2F3136) # now make an embed with the final result
        embed.set_thumbnail(url=self.botdata.uris["candy"])
        await ctx.send(embed=embed) # send it


def setup(bot):
    bot.add_cog(Candy(bot))
