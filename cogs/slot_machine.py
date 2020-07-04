import discord

import random
import asyncio
import json

from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from .utils.data import BotData, isBlacklisted


class SlotMachine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.botdata = BotData(self.bot)

    # The slot machine command.
    # <summary>
    #   this command is a slot machine built in discord..
    # </summary>
    @commands.command()
    @commands.cooldown(1, 20.0, BucketType.guild)
    @isBlacklisted()
    async def slot(self, ctx):

        # setup a list of choices
        choices = [
            ":seven:",
            ":pineapple:",
            ":grapes:",
            ":cherries:",
            ":banana:",
            ":lemon:",
        ]

        # func to check how many slots are equal
        def isEqual(x, y, z):
            result = set([x, y, z])
            if len(result) == 3:
                return 0
            else:
                return 4 - len(result)

        slot1 = random.choice(choices) # pick the first slot
        slot2 = random.choice(choices) # pick the second slot
        slot3 = random.choice(choices) # pick the third slot

        with open("db/slotdb.json", "r") as f:
            l = json.load(f) # load the coins

        earning = 0

        try:
            balance = l[str(ctx.author.id)]  # Try incrementing the balance by 5 to see if it exists
        except KeyError:
            balance = l[str(ctx.author.id)] = 5  # If it doesn't, make it 5

        if balance - 2 < 0:
            return await ctx.send(
                "You don't have enough coins! Buy some more at the shop."
            )

        balance -= 2

        pembed = await ctx.send(
            embed=discord.Embed(
                title="Slot Machine", description="Spinning Slots.", color=0x2F3136
            ).set_thumbnail(url=self.botdata.uris["slot-machine"])
        ) # send the first embed

        # the block below edits the `.`. yeah, its for no reason but why not
        for i in range(3):
            embed = discord.Embed(
                title="Slot Machine",
                description=f"Spinning Slots {'.'*i}",
                colour=0x2F3136,
            )
            embed.set_thumbnail(url=self.botdata.uris["slot-machine"])
            await pembed.edit(embed=embed)
            await asyncio.sleep(0.3)

        # below we edit the embed to show the slot results.
        embed = discord.Embed(
            title="Slot Machine", description=f"{slot1} ? ?", colour=0x2F3136
        )
        embed.set_thumbnail(url=self.botdata.uris["slot-machine"])
        await pembed.edit(embed=embed)
        await asyncio.sleep(0.5)

        embed = discord.Embed(
            title="Slot Machine", description=f"{slot1} {slot2} ?", colour=0x2F3136
        )
        embed.set_thumbnail(url=self.botdata.uris["slot-machine"])
        await pembed.edit(embed=embed)
        await asyncio.sleep(0.5)

        testEq = isEqual(slot1, slot2, slot3)

        # the statements below check the equality between the slots.
        if testEq == 3:
            embed = discord.Embed(
                title="Winner! (3 identical slots) - $30",
                description=f"{slot1} {slot2} {slot3}",
                colour=0x2F3136,
            )
            embed.set_thumbnail(url=self.botdata.uris["slot-machine"])
            earning = 30 # set the earning to `30` if all three slots are equal
        elif testEq == 0:
            embed = discord.Embed(
                title="Better luck next time! (0 identical slots) - $-5",
                description=f"{slot1} {slot2} {slot3}",
                colour=0x2F3136,
            )
            embed.set_thumbnail(url=self.botdata.uris["slot-machine"])
            earning = -5 # set the earing to `-5` if all slots are unequal
        else:
            embed = discord.Embed(
                title="Winner! (2 identical slots) - $15",
                description=f"{slot1} {slot2} {slot3}",
                colour=0x2F3136,
            )
            embed.set_thumbnail(url=self.botdata.uris["slot-machine"])
            earning = 15 # set the earning to `15` if two slots are equal

        l[str(ctx.author.id)] += earning # increase the balance by teh earning
        balance = l[str(ctx.author.id)]

        with open("db/slotdb.json", "w") as f:
            json.dump(l, f, indent=4) # save the changes

        embed.add_field(name="Balance", value=str(balance), inline=False)
        await pembed.edit(embed=embed) # send the embed.


def setup(bot):
    bot.add_cog(SlotMachine(bot))
