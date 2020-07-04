import discord

from discord.ext import commands

from .utils.data import BotData, isBlacklisted


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.botdata = BotData(self.bot)

    # A blacklist command. I don't have to explain this, really.
    # Nothing interesting here.
    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, member: discord.Member):
        if member.id not in self.botdata.blacklist:
            self.botdata.blacklist.append(member.id)
            await ctx.send("Member blacklisted,")
        else:
            await ctx.send("Member already blacklisted.")

    # Same for this command, nothing interesting..
    @commands.command()
    @commands.is_owner()
    async def whitelist(self, ctx, member: discord.Member):
        if member.id not in self.botdata.blacklist:
            self.botdata.blacklist.pop(self.botdata.blacklist.index(member.id))
            await ctx.send("Member whitelisted.")
        else:
            await ctx.send("Member is not in blacklist.")


def setup(bot):
    bot.add_cog(Admin(bot))
# and the end of the cog, wow :p
