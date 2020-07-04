import discord

import json

from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands, menus

from .utils.data import BotData


# Shop Source is a class that inherits a menu. this will allow us to create a paginator.
class ShopSource(menus.ListPageSource):
    async def format_page(self, menu, page):
        if isinstance(page, str):
            embed = discord.Embed(
                title=f"Shop",
                description="To buy an item, type `arcade shop buy <item>`"
                + "".join(page),
                color=0x2F3136,
            )
            return embed
        else:
            embed = discord.Embed(
                title=f"Shop",
                description=f"To buy an item, type `arcade shop buy <item>`"
                + "\n".join(page),
                color=0x2F3136,
            )
            return embed


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.botdata = BotData(self.bot)

    # The balance command.
    # <summary>
    #   this command will display a players current balance.
    #   it will display both candy, and coins.
    # </summary>
    @commands.command()
    @commands.cooldown(1, 10.0, BucketType.user)
    async def balance(self, ctx, member: discord.Member = None):
        if member is None: # if the member is not specified,
            member = ctx.author # the member is the author.

        with open("db/slotdb.json", "r") as f:
            l = json.load(f) # load the coins

        with open("db/candylb.json", "r") as f:
            l2 = json.load(f) # load the candy

        try:
            cur = l[str(member.id)] # get the members coins
        except KeyError:
            cur = 0 # if their balance does not exist, set it to 0
        try:
            cur2 = l2[str(member.id)] # get the members candy
        except KeyError:
            cur2 = 0 # if their balance does not exist, set it to 0

        embed = discord.Embed(
            title="Balance", description="Here is your balance", colour=0x2F3136
        ) # set the embed
        embed.add_field(name="Slot Machine Coins:", value=f"{cur}", inline=True) # add a coin bal field
        embed.add_field(name="Candy:", value=f"{cur2}", inline=True) # add a candy bal field
        embed.set_thumbnail(url=self.botdata.uris["coin"])
        await ctx.send(embed=embed) # send the message

    # The shop command.
    # <summary>
    #   this command will display the shop and the purchaseable items.
    # </summary>
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 30.0, BucketType.user)
    async def shop(self, ctx):
        with open("db/shop.json", "r") as f:
            l = json.load(f) # load the shop

        coin_items = ""

        # for some reason, i put this in a function.
        # i couldn't find any other way to do it i guess..
        def get_coin_keys():
            x = ""
            for k, v in l["coins"].items():
                x += f"{k}: ${v}\n"

            return x

        coin_items = get_coin_keys() # set the coin items

        candy_items = ""

        for i in l["candy"].keys():
            for x in l["candy"].values():
                candy_items += f"{i}: {x}:candy: " # add the candy items.

        pages = [
            f"""
        **Candy:**
        {candy_items}
        """,
            f"""
        **Coins:**
        {coin_items}
        """,
        ] # set the pages that you can scroll through.

        source = ShopSource(pages, per_page=1)
        menu = menus.MenuPages(source)
        await menu.start(ctx) # send the message and start the paginator.

    # The buy command.
    # <summary>
    #   in this command, you can buy items from the shop.
    #   this includes both candy items, and coin items.
    # </summary>
    @shop.command()
    @commands.cooldown(1, 10.0, BucketType.user)
    async def buy(self, ctx, *item: str):
        item = " ".join(item)
        with open("db/shop.json", "r") as f:
            l = json.load(f) # load the shop

        with open("db/slotdb.json", "r") as f:
            l2 = json.load(f) # load the coins

        with open("db/candylb.json", "r") as f:
            l3 = json.load(f) # load the candy

        with open("db/profile.json", "r") as f:
            l4 = json.load(f) # load the players profile

        # if the item is not in the shop
        if item not in str(l["candy"].keys()) and item not in str(l["coins"].keys()):
            return await ctx.send("Sorry, that item does not exist!") # tell them and exit the command.

        # the whole chunk below is for buying badges.
        # it checks if they have enough for the badge,
        # and if they already have this badge.
        # it also checks if they have a profile because badges get added
        # to their profiles.
        try:
            if "Badge" in item:
                if self.botdata.badges[item] in l4[str(ctx.author.id)]["Badges"]:
                    return await ctx.send("Sorry, you already have this badge!")
                if l2[str(ctx.author.id)] - l["coins"][item] < 0:
                    return await ctx.send(
                        "Sorry, you dont't have enough money for this badge!"
                    )
                else:
                    l2[str(ctx.author.id)] -= l["coins"][item]
                    with open("db/slotdb.json", "w") as f:
                        json.dump(l2, f, indent=4)

                    l4[str(ctx.author.id)]["Badges"][item] = self.botdata.badges[item]

                    with open("db/profile.json", "w") as f:
                        json.dump(l4, f, indent=4)

        except KeyError:
            return await ctx.send(
                "\
Sorry, you don't have an account, you don't have any coins, or that item does not exist!\
 To open an account, type `arc profile create`.\
 To get coins, play with the slot machine."
            )
        else:
            embed = discord.Embed(
                title="Bought Item Successfully!",
                description=f"Successfully bought {item}!",
                colour=0x2F3136,
            )

            embed.add_field(
                name="Current Balance (Candy)",
                value=str(l3[str(ctx.author.id)]),
                inline=True,
            )

            embed.add_field(
                name="Current Balance (Coins)",
                value=str(l2[str(ctx.author.id)]),
                inline=True,
            )
            embed.set_thumbnail(url=self.botdata.uris["shop"])
            return await ctx.send(embed=embed)

        # this block checks if the item is in the coins section.
        # it also checks if they have enough coins to buy the item.
        if item in l["coins"]:
            try:
                if not l2[str(ctx.author.id)] - l["coins"][item] < 0:
                    l2[str(ctx.author.id)] -= l["coins"][item]
                else:
                    return await ctx.send(
                        "Sorry, you don't have any coins! Get some more by playing the with the slot machine."
                    )
            except KeyError:
                return await ctx.send(
                    "Sorry, you don't have any coins! Get some more by playing with the slot machine."
                )

            else:
                with open("db/slotdb.json", "w") as f:
                    json.dump(l2, f, indent=4)

        # this block checks if the item is in the candy section.
        # it also checks if they have enough candy to buyt the item.
        elif item in l["candy"]:
            try:
                if not l3[str(ctx.author.id)] - l["candy"][item] < 0:
                    l3[str(ctx.author.id)] -= l["candy"][item]
                else:
                    return await ctx.send(
                        "Sorry, you don't have enough candy! Get some more by playing the Candy game."
                    )
            except KeyError:
                return await ctx.send(
                    "Sorry, you don't have any candy! Get some more by playing the Candy game."
                )

            else:
                with open("db/candy.json", "w") as f:
                    json.dump(l3, f, indent=4)

        embed = discord.Embed(
            title="Bought Item Successfully!",
            description=f"Successfully bought {item}!",
            colour=0x2F3136,
        ) # create a ne embed.

        embed.add_field(
            name="Current Balance (Candy)",
            value=str(l3[str(ctx.author.id)]),
            inline=True,
        ) # add the current balance field for candy

        embed.add_field(
            name="Current Balance (Coins)",
            value=str(l2[str(ctx.author.id)]),
            inline=True,
        ) # add the current balance field for coins
        embed.set_thumbnail(url=self.botdata.uris["shop"])
        await ctx.send(embed=embed) # send the embed


def setup(bot):
    bot.add_cog(Economy(bot))
