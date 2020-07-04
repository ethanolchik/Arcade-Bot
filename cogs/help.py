import discord

from discord.ext import commands, menus
from discord.ext.commands.cooldowns import BucketType

from .utils.data import BotData, isBlacklisted


class HelpSource(menus.ListPageSource):
    async def format_page(self, menu, page):
        if isinstance(page, str):
            embed = discord.Embed(
                title=f"Help",
                description="(When using commands, <> indicates a required argument and [] indicates an optional argument.) do **NOT** include them when using commands."
                + "".join(page),
                color=0x2F3136,
            )
            return embed
        else:

            embed = discord.Embed(
                title=f"Help",
                description=f"(When using commands, <> indicates a required argument and [] indicates an optional argument.) do **NOT** include them when using commands."
                + "\n".join(page),
                color=0x2F3136,
            )
            return embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.botdata = BotData(self.bot)

    # The help command.
    # <summary>
    #   this command sends information about a given command to the user.
    #   if no command given, it will give them help for every command.
    # </summary>
    @commands.command()
    @commands.cooldown(1, 5.0, BucketType.channel)
    @isBlacklisted()
    async def help(self, ctx, command: str = None):
        prefix = "arc!"
        error = f'```css\nThat command, "{command}", does not exist!\n```'
        if command: # check if the command exists
            embed = discord.Embed(title="Help", colour=0x2F3136) #  create a new embed
            cmd = self.bot.get_command(command) # get the command description.

            if not cmd:
                if command == "ttt": # tic tac toe is in js, so the python side doesn't know it exists.
                    # this means we have to add it manually.
                    embed.add_field(
                        name="Usage:",
                        value=f"{prefix}ttt [member]",
                        inline=False,
                    )
                    return await ctx.send(embed=embed) # send the help for tic tac toe
                else:
                    return await ctx.send(error) # if its not tic tac toe, tell the user that the command does not exist.

            # check that the command is not hidden
            if not cmd.hidden:
                
                # this whole block below is for sub-commands,
                # aliases and such. to save myself time, im not gonna go through this.
                if cmd.parent:

                    embed.add_field(
                        name="Usage:",
                        value=f"{prefix}{cmd.parent} {cmd.name} {cmd.signature}",
                        inline=False,
                    )
                else:

                    embed.add_field(
                        name="Usage:",
                        value=f"{prefix}{cmd.name} {cmd.signature}",
                        inline=False,
                    )

                if cmd.aliases:

                    aliases = ""

                    for a in cmd.aliases:
                        aliases += f"\n`{a}`"

                    embed.add_field(name="Aliases", value=aliases, inline=False)

                try:

                    commands = ""

                    for a in cmd.commands:
                        commands += f"`{prefix}{cmd.name} {a.name} {a.signature}`\n"

                    embed.add_field(name="Subcommands", value=commands, inline=False)

                except:

                    pass

            else:

                await ctx.send(error)
                return

            await ctx.send(embed=embed)
            return

        # these chunks below set up the default help command for the bot.
        con4 = ""
        for a in self.bot.commands:
            if a.cog_name == "Connect4":
                if not a.hidden:
                    con4 += f"`{prefix}{a.name}` ◍ "
                    try:
                        for b in a.commands:
                            con4 += f"`{prefix}{a.name} {b.name}` ◍ "
                    except:
                        pass

        slot = ""
        for a in self.bot.commands:
            if a.cog_name == "SlotMachine":
                if not a.hidden:
                    slot += f"`{prefix}{a.name}` ◍ "
                    try:
                        for b in a.commands:
                            slot += f"`{prefix}{a.name} {b.name}` ◍ "
                    except:
                        pass

        economy = ""
        for a in self.bot.commands:
            if a.cog_name == "Economy":
                if not a.hidden:
                    economy += f"`{prefix}{a.name}` ◍ "
                    try:
                        for b in a.commands:
                            economy += f"`{prefix}{a.name} {b.name}` ◍ "
                    except:
                        pass

        candy = ""
        for a in self.bot.commands:
            if a.cog_name == "Candy":
                if not a.hidden:
                    candy += f"`{prefix}{a.name}` ◍ "
                    try:
                        for b in a.commands:
                            candy += f"`{prefix}{a.name} {b.name}` ◍ "
                    except:
                        pass

        profs = ""
        for a in self.bot.commands:
            if a.cog_name == "Profiles":
                if not a.hidden:
                    profs += f"`{prefix}{a.name}` ◍ "
                    try:
                        for b in a.commands:
                            profs += f"`{prefix}{a.name} {b.name}` ◍ "
                    except:
                        pass

        fdescriptions = [
            f"""
            **Connect Four**
            {con4}
            """,
            f"""
            **Slot Machine**
            {slot}
            """,
            f"""
            **Economy**
            {economy}
            """,
            f"""
            **Candy**
            {candy}
            """,
            f"""
            **Profiles**
            {profs}
            """,
            f"""
            **Tic Tac Toe**
            `{prefix}ttt` ◍ 
            """
        ] # format the help command into a list

        source = HelpSource(fdescriptions, per_page=2) # paginate it
        menu = menus.MenuPages(source)
        await menu.start(ctx) # send the paginator

    # The info command.
    # <summary>
    #   this command will display information about the bot.
    # </summary>
    @commands.command(aliases=["about"])
    @commands.cooldown(1, 5.0, BucketType.channel)
    @isBlacklisted()
    async def info(self, ctx):
        embed = discord.Embed(
            title="About",
            description=f"I was made by {self.bot.get_user(self.bot.owner_id)}.",
            colour=0x2F3136,
        )
        embed.add_field(
            name="Written in:", value=f"Discord.py {discord.__version__}", inline=True
        )
        embed.add_field(name="Bot Version:", value="0.0.1", inline=True)
        embed.set_thumbnail(url=self.botdata.uris["profile"])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
