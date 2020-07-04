import discord
from discord.ext import commands

# Here, we will keep all of the bots data used in most of the cogs.
# Don't mind it being messy, i just didn't wanna ruin the links ;)
class BotData:
    def __init__(self, bot):
        self.bot = bot
        # Bot URL's. Stuff like the bots avatar URL and the embed icons go here.
        self.uris = {
            "shop": "https://cdn.discordapp.com/attachments/661654841231278103/727168933076926584/Arcade_Bot_Shop.jpg",
            "profile": "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.{1}".format(
                self.bot.user, "png"
            ),
            "slot-machine": "https://cdn.discordapp.com/attachments/661654841231278103/727170018575384647/Arcade_Bot_Slot_Machine.jpg",
            "candy": "https://cdn.discordapp.com/attachments/661654841231278103/727175816773107793/Arcade_Bot_Candy.png",
            "coin": "https://cdn.discordapp.com/attachments/661654841231278103/727174237034512404/Arcade_Bot_Coin.jpg",
        }
        # Badges. these are given to the player by purchasing them in the shop.
        self.badges = {
            "Iron Badge": "<:IronBadge:727216782989066241>",
            "Bronze Badge": "<:BronzeBadge:727215148321996821>",
            "Silver Badge": "<:SilverBadge:727216852710850613>",
            "Gold Badge": "<:GoldenBadge:727216755713507508>",
            "Platinum Badge": "<:PlatinumBadge:727216810352705627>",
            "Diamond Badge": "<:DiamondBadge:727216704005996654>",
            "Champion Badge": "<:ChampionBadge:727217115588984913>",
        }
        # And of course, a staff badge.
        # `Why?` you ask? Why not :p
        self.staff_badge = "<:StaffBadge:727218894313357382>"

    # And of course, a blacklist.
    blacklist: list = [700091773695033505]

# A custom check that makes sure a person in the bots blacklist cannot use any command
# that this check is applied to.
def isBlacklisted():
    async def pred(ctx):
        return ctx.author.id not in BotData.blacklist

    return commands.check(pred)
