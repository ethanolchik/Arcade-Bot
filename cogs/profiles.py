import discord

import json

from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from .utils.data import *


class Profiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.botdata = BotData(self.bot)

    # The profile command.
    # <summary>
    #   this command displays information about the users profile. of course, this is ingame.
    # </summary>
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10.0, BucketType.user)
    @isBlacklisted()
    async def profile(self, ctx):
        with open("db/profile.json", "r") as f:
            l = json.load(f) # load the profiles

        with open("db/candylb.json", "r") as f:
            l2 = json.load(f) # load the candy

        with open("db/slotdb.json", "r") as f:
            l3 = json.load(f) #  load the coins
        badges = ""
        candy = ""
        coins = ""
        try:
            try:
                print(l[str(ctx.author.id)]["Badges"])
            except KeyError:
                badges = None
            else:
                badges = (
                    str(l[str(ctx.author.id)]["Badges"].values())
                    .replace("dict_values([", "")
                    .replace("'", "")
                    .replace(",", "")
                    .replace("]", "")
                    .replace(")", "")
                ) # haha, string manipulation go brrr. hey, at least it's neat.
            print(l[str(ctx.author.id)])
        except KeyError:
            return await ctx.send(
                "Sorry, you don't have a profile yet! Create one by using `arc profile create`."
            )
        else:
            embed = discord.Embed(
                title="Profile",
                description=f"{ctx.author.mention}'s profile",
                colour=0x2F3136,
            ) # create the embed
            embed.add_field(name="Badges:", value=badges, inline=False) # display the users badges
            try:
                candy = (str(l2[str(ctx.author.id)])) # check if they have a candy balance
            except KeyError:
                candy = None
            else:
                embed.add_field(name="Candy:", value=candy[0], inline=False) # display users candy bal
            try:
                coins = str(l3[str(ctx.author.id)]) # check if they have a coin balance
            except KeyError:
                coins = None
            else:
                embed.add_field(name="Coins:", value=str(coins), inline=False) # display coin bal
            embed.set_thumbnail(url=ctx.author.avatar_url_as(static_format="png"))
            await ctx.send(embed=embed) # send the embed

    # The create command.
    # <summary>
    #   this command will create a profile for the user.
    # </summary>
    @profile.command()
    @commands.cooldown(1, 3600, BucketType.user)
    @isBlacklisted()
    async def create(self, ctx):
        with open("db/profile.json", "r") as f:
            l = json.load(f) # load profiles

        try:
            print(l[str(ctx.author.id)]["Badges"]) # try printing their badges
        except KeyError:
            l[str(ctx.author.id)] = {}
            l[str(ctx.author.id)]["Badges"] = {}
        else:
            return await ctx.send("Sorry, you already have a profile!") # if this doesn't raise a `KeyError`, 
            # they already have a profile

        embed = discord.Embed(
            title="Profile Created!",
            description="Successfully Created Your Profile!",
            colour=0x2F3136,
        ) # create teh embed

        with open("db/profile.json", "w") as f:
            json.dump(l, f, indent=4) # save changes in profiles

        await ctx.send(embed=embed) # send the embed


def setup(bot):
    bot.add_cog(Profiles(bot))
