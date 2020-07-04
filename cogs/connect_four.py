import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

import asyncio

from c4_game import Connect4Game

from .utils.data import BotData, isBlacklisted


class Connect4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    CANCEL_GAME_EMOJI = "🚫"
    DIGITS = [
        str(digit) + "\N{combining enclosing keycap}" for digit in range(1, 8)
    ] + ["🚫"]
    VALID_REACTIONS = [CANCEL_GAME_EMOJI] + DIGITS
    GAME_TIMEOUT_THRESHOLD = 60

    # the Connect Four command
    # <summary>
    #   this command hosts a connect four game on discord.
    #   it allows the user to play with one other person.
    #   the winner is the one who can get 4 pieces in a row.
    #   if all of the columns are full, its a tie.
    # </summary>
    @commands.command(aliases=["c4", "conn4"])
    @commands.max_concurrency(1, per=BucketType.guild, wait=True)
    @isBlacklisted()
    async def connect4(self, ctx, player2: discord.Member = None):
        if player2 is None: # check if the user mentioned a second player.
            return await ctx.send("Please specify a member to play with!") # if they didn't, tell them and end the command.
        player1 = ctx.author

        if player2.id == player1.id: # if the second player is the first player,
            return await ctx.send("You can't play connect 4 with yourself!") # tell them and end the command.

        game = Connect4Game(player1.display_name, player2.display_name) # create an instance of the game.
        embed = discord.Embed(
            title="Connect Four", description=str(game), colour=0x2F3136
        ) # create the embed
        embed.set_thumbnail(url=self.bot.user.avatar_url_as(static_format="png"))
        message = await ctx.send(embed=embed) # send it.

        for digit in self.DIGITS:
            await message.add_reaction(digit) # add the digit (column number) reactions.

        def check(reaction, user):
            return (
                user == (player1, player2)[game.get_turn() - 1] # check that its the `reactor` is the current player
                and str(reaction) in self.VALID_REACTIONS # check that the reaction is a valid reaction. (its a reaction added by the bot)
                and reaction.message.id == message.id # check that the message id is the same as the message that the reaction was added to.
            )

        while game.get_winner() == game.NO_WINNER: # while there is no winner
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=self.GAME_TIMEOUT_THRESHOLD
                ) # add the reactions
            except asyncio.TimeoutError:
                game.forfeit() # if they run out of time, forfeit for them.
                break # exit the loop.

            await asyncio.sleep(0.2)
            try:
                await message.remove_reaction(reaction, user) # try to remove their reaction
            except discord.errors.Forbidden: # if we can't, (permission error)
                pass # do nothing and continue with the command.

            if str(reaction) == self.CANCEL_GAME_EMOJI: # if the reaction is the `cancel` emoji,
                game.forfeit()  # forfeit the game.
                break # exit the loop.

            try:
                game.move(self.DIGITS.index(str(reaction))) # try to move their piece 
            except ValueError:
                pass # if we get a ValueError, dont do anything and continue the game.
            embed = discord.Embed(
                title="Connect Four", description=str(game), colour=0x2F3136
            )
            embed.set_thumbnail(url=self.bot.user.avatar_url_as(static_format="png"))
            await message.edit(embed=embed) # send the new embed.

        await self.end_game(game, message) # when we exit the loop, quit the game.

    @classmethod
    async def end_game(cls, game, message):
        embed = discord.Embed(
            title="Connect Four", description=str(game), colour=0x2F3136
        ) # create the new, and final embed.
        await message.edit(embed=embed) # edit the message to show the winner.
        await cls.clear_reactions(message) # clear the reactions.

    @staticmethod
    async def clear_reactions(message):
        try:
            await message.clear_reactions() # clear the reactions
        except discord.HTTPException:
            pass # if we cant, dont do anything.


def setup(bot):
    bot.add_cog(Connect4(bot))

# NOTE: check out ../c4_game.py to see where the actual `base` of the connect 4 game comes from.
