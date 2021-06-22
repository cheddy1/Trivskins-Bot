import discord
import sqlite3
import time
from discord.ext import commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument

connection = sqlite3.connect('Trivskins.db')
cursor = connection.cursor()

gain_rate = 60  # how frequently users can gain coins in seconds
gain_amount = 1  # how many coins users gain per rate


# Check if the user is able to gain more xp at that time
async def valid_gain(xp_time):
    difference = int(time.time()) - xp_time
    if difference < gain_rate:
        return False
    else:
        return True


class Currency(commands.Cog, name="Currency"):

    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect("Trivskins.db")
        self.c = self.connection.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, name text NOT NULL, xp integer NOT NULL, xp_time integer NOT NULL)''')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        guild = ctx.guild
        if guild is None:
            return
        if ctx.author == self.bot.user:
            return

        user_id = int(ctx.author.id)
        name = str(ctx.author)
        xp = 0
        xp_time = int(time.time())

        # If this is the users first time chatting, insert them into the table
        self.c.execute('''INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)''', (user_id, name, xp, xp_time))
        self.connection.commit()

        # Check if the user is on cooldown
        if await valid_gain(self.c.execute('''SELECT xp_time FROM users WHERE id=?''', (user_id,)).fetchone()[0]):

            # Add xp to user (coins)
            self.c.execute('''UPDATE users SET xp = xp + ?, xp_time=? WHERE id=?''', (gain_amount, xp_time, user_id))
            self.connection.commit()

    # Check how many coins a user has
    @commands.command(aliases=['balance', 'money', 'currency'])
    async def bal(self, ctx, *args):

        # Only check one user at a time
        if len(args) > 1:
            return await ctx.message.add_reaction('\U0000274C')

        # Check if the user they @ed is valid, if it even was a user
        if args:
            try:
                user_id = args[0].replace('<@', '').replace('>', '')
                user = await self.bot.fetch_user(user_id)
            except:
                return await ctx.message.add_reaction('\U0000274C')

        # Default user is the user that called the command
        else:
            user_id = ctx.author.id
            user = self.bot.get_user(user_id)

        # Get the amount of coins the user has
        coins = self.c.execute('''SELECT xp FROM users WHERE id=?''', (user_id,)).fetchone()
        if coins:

            # Create and send the bal embed message
            embed_desc = user.mention + ' currently has __**' + str(coins[0]) + '**__ coins!'
            embed = discord.Embed(title="Coin Balance", description=embed_desc, color=0XA60B00)
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text='Use !coins help to see what you can buy!')
            return await ctx.message.channel.send(embed=embed)
        else:
            return await ctx.message.add_reaction('\U0000274C')

    # Coins help commands for users and admins
    @commands.command()
    async def coins(self, ctx, *args):
        if 'admin' in args:
            embed_desc = '!editcoins **give** @user #amount\n!editcoins **remove** @user #amount\n!editcoins **set** @user #amount\n!editcoins **reset** @user'
            embed = discord.Embed(title="Admin Panel", description=embed_desc, color=0X2C3675)
        else:
            embed_desc = 'Coins are Trivskins Trading server currency. You can use them to buy a variety of different things. You gain one coin every message you send (max one per minute).'
            embed_shop = '!buy ticket (#amount) (giveaway_name) - Buy giveaway entry tickets'
            embed = discord.Embed(title="Coins Help", description=embed_desc, color=0X2C3675)
            embed.add_field(name="Shop", value=embed_shop, inline=False)
        await ctx.message.channel.send(embed=embed)

    # Shop command to allow users to spend their coins
    @commands.command()
    async def buy(self, ctx, item, amount, *args):

        if args[0] == 'ticket' and len(args) == 3:

            await ctx.message.channel.send("Sorry but giveaways have not yet been enabled. Please check back soon!")

        else:
            return await ctx.message.add_reaction('\U0000274C')

    # Admin command to edit someones coins
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def editcoins(self, ctx, command, *args):

        # Adds a set amount of coins to a user
        if command.lower() == 'give' and len(args) == 2:
            user_id = args[0].replace('<@', '').replace('>', '')
            if self.c.execute('''SELECT 1 FROM users WHERE id=?''', (user_id,)).fetchone():
                self.c.execute('''UPDATE users SET xp = xp+? WHERE id=?''', (args[1], user_id))
                self.connection.commit()
                return await ctx.message.add_reaction('\U00002705')
            else:
                return await ctx.message.add_reaction('\U0000274C')

        # Removes a set amount of coins from a user
        elif command.lower() == 'remove' and len(args) == 2:
            user_id = args[0].replace('<@', '').replace('>', '')
            if self.c.execute('''SELECT 1 FROM users WHERE id=?''', (user_id,)).fetchone():
                self.c.execute('''UPDATE users SET xp = xp-? WHERE id=?''', (args[1], user_id))
                self.connection.commit()
                return await ctx.message.add_reaction('\U00002705')
            else:
                return await ctx.message.add_reaction('\U0000274C')

        # Sets a users balance to a certain amount
        elif command.lower() == 'set' and len(args) == 2:
            user_id = args[0].replace('<@', '').replace('>', '')
            if self.c.execute('''SELECT 1 FROM users WHERE id=?''', (user_id,)).fetchone():
                self.c.execute('''UPDATE users SET xp=? WHERE id=?''', (args[1], user_id))
                self.connection.commit()
                return await ctx.message.add_reaction('\U00002705')
            else:
                return await ctx.message.add_reaction('\U0000274C')

        # Resets a users balance to 0
        elif command.lower() == 'reset' and len(args) == 1:
            user_id = args[0].replace('<@', '').replace('>', '')
            if self.c.execute('''SELECT 1 FROM users WHERE id=?''', (user_id,)).fetchone():
                self.c.execute('''UPDATE users SET xp=0 WHERE id=?''', (user_id,))
                self.connection.commit()
                return await ctx.message.add_reaction('\U00002705')
            else:
                return await ctx.message.add_reaction('\U0000274C')

        else:
            return await ctx.message.add_reaction('\U0000274C')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        error = getattr(error, "original", error)
        if isinstance(error, MissingPermissions) or isinstance(error, MissingRequiredArgument):
            return await ctx.message.add_reaction('\U0000274C')
        else:
            raise error


def setup(bot):
    bot.add_cog(Currency(bot))
