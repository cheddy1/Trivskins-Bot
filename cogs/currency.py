import discord
import sqlite3
import random
import time
import asyncio
from discord.ext import commands
from discord.ext.commands import MissingPermissions, MissingRequiredArgument
import difflib

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
        if guild is None or ctx.author == self.bot.user or ctx.author.bot:
            return
        user_id = int(ctx.author.id)
        name = str(ctx.author)
        xp = 1
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

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx):
        all_user_list = self.c.execute('''SELECT name, xp FROM users ORDER BY xp DESC''').fetchall()
        embed_desc = ''
        ten_count = 1
        total_count = 0
        place_count = 0
        continue_counting = True
        top_ten_list = all_user_list[:10]
        for user in top_ten_list:
            embed_desc += str(ten_count) + '. ' + user[0] + ' - **' + str(user[1]) + '** \U0001FA99 \n'
            ten_count += 1
        for user in all_user_list:
            total_count += 1
            if user[0] == str(ctx.message.author) and continue_counting:
                place_count = total_count
                continue_counting = False

        embed = discord.Embed(title="Coins Leaderboard", description=embed_desc, color=0Xfcba03)
        embed.set_footer(text='Your rank: ' + str(place_count) + '/' + str(total_count))
        await ctx.message.channel.send(embed=embed)

    @commands.command(aliases=['hl'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def highlow(self, ctx, *args):
        if not args:
            await ctx.message.add_reaction('\U0000274C')
            return await ctx.message.channel.send("Missing amount of coins to gamble. `!coinflip (amount)`")
        else:
            seed = random.randint(0, 100)
            embed_desc = 'M number number is **__' + str(seed) + '__**\nPress \U00002B06 if you think your number will be higher\nPress \U00002B07 if you think your number will be lower'
            embed = discord.Embed(title="High Low", description=embed_desc, color=0Xfcba03)
            embed_highlow = await ctx.message.channel.send(embed=embed)
            await embed_highlow.add_reaction('\U00002B06')
            await embed_highlow.add_reaction('\U00002B07')

            try:
                userchoice, user = await self.bot.wait_for('reaction_add', check=lambda message: message.author == ctx.author, timeout=30)
            except asyncio.TimeoutError:
                await embed_highlow.add_reaction
                await ctx.message.channel.send("Timed out!")
                return


    # Shop command to allow users to spend their coins
    @commands.command()
    async def buy(self, ctx, item, amount, *args):
        if item == 'ticket':
            try:
                amount = int(amount)
            except ValueError:
                await ctx.message.add_reaction('\U0000274C')
                return await ctx.message.channel.send("Invalid input. Try `!buy ticket (amount) (giveaway name)`")
            giveaways = self.c.execute('''SELECT name FROM giveaways''').fetchall()
            if len(giveaways) > 1:
                result = ', '.join(item[0] for item in giveaways)
                if args:
                    giveaway_name = ' '.join(args)
                    giveaway_name = str(difflib.get_close_matches(giveaway_name, result.split(","), 1, .4)[0]).strip()
                else:
                    await ctx.message.add_reaction('\U0000274C')
                    return await ctx.message.channel.send("You must specify the giveaway name because there are multiple giveaways running currently. Use `!buy ticket (amount) (giveaway name)`\nCurrently open: **" + result+ "**")
            elif len(giveaways) == 1:
                giveaway_name = giveaways[0][0]
            else:
                await ctx.message.channel.send("There are no giveaways currently!")
                return await ctx.message.add_reaction('\U0000274C')
            if not giveaway_name:
                await ctx.message.add_reaction('\U0000274C')
                return await ctx.message.channel.send("A giveaway with that name does not exist! Currently running giveaways: " + ', '.join(giveaways))
            user_id = ctx.message.author.id
            giveaway_info = self.c.execute('''SELECT ticket_cost, ticket_max FROM giveaways WHERE name=?''', (giveaway_name,)).fetchone()
            user_tickets = self.c.execute('''SELECT tickets FROM entries WHERE name=? AND id=?''', (giveaway_name, user_id)).fetchone()
            total_cost = amount * int(giveaway_info[0])
            current_bal = self.c.execute('''SELECT xp FROM users WHERE id=?''', (user_id,)).fetchone()
            while True:
                if not current_bal:
                    await ctx.message.add_reaction('\U0000274C')
                    return await ctx.message.channel.send("Please send a message before attempting to buy, you haven't been added to my database yet!")
                if total_cost > current_bal[0]:
                    total_cost = total_cost - int(giveaway_info[0])
                    amount = amount - 1
                elif amount == 0:
                    await ctx.message.add_reaction('\U0000274C')
                    return await ctx.message.channel.send("You do not have enough coins to buy any tickets, sorry!")
                else:
                    break
            if not user_tickets:
                if amount > giveaway_info[1]:
                    amount = giveaway_info[1]
                self.c.execute('''INSERT OR IGNORE INTO entries VALUES (?, ?, ?)''', (giveaway_name, user_id, amount))
                self.connection.commit()
                print(self.c.execute('''SELECT * FROM entries ''').fetchall())
            else:
                if int(user_tickets[0]) >= giveaway_info[1]:
                    await ctx.message.add_reaction('\U0000274C')
                    return await ctx.message.channel.send("You already have the max number of tickets for this giveaway!")
                if (amount + user_tickets[0]) > giveaway_info[1]:
                    amount = int(giveaway_info[1])
                self.c.execute('''UPDATE entries SET tickets = tickets + ? WHERE name=? AND id=?''', (amount, giveaway_name, user_id))
                self.connection.commit()
            self.c.execute('''UPDATE users SET xp = xp - ? WHERE id=?''', (total_cost, user_id))
            self.connection.commit()
            user_tickets = self.c.execute('''SELECT tickets FROM entries WHERE name=? AND id=?''', (giveaway_name, user_id)).fetchone()
            entries = self.c.execute('''SELECT tickets FROM entries WHERE name=?''', (giveaway_name,)).fetchall()
            num_tickets = 0
            for ticket in entries:
                num_tickets = num_tickets + int(ticket[0])
            await ctx.message.channel.send("You bought **" + str(amount) + "** tickets for **" + str(giveaway_name) + "**.\nYou have **" + str(user_tickets[0]) + "** tickets for this giveaway. (Max of **" + str(giveaway_info[1]) + "**)\nThere are **"+ str(num_tickets) + "** entries so far in this giveaway.")
            return await ctx.message.add_reaction('\U00002705')
        else:
            return await ctx.message.add_reaction('\U0000274C')

    # Admin command to edit someones coins
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def editcoins(self, ctx, command, *args):

        # Adds a set amount of coins to a user
        if command.lower() == 'give' and len(args) == 2:
            user_id = args[0].replace('<@', '').replace('!','').replace('>', '')
            if self.c.execute('''SELECT 1 FROM users WHERE id=?''', (user_id,)).fetchone():
                self.c.execute('''UPDATE users SET xp = xp+? WHERE id=?''', (args[1], user_id))
                self.connection.commit()
                return await ctx.message.add_reaction('\U00002705')
            else:
                return await ctx.message.add_reaction('\U0000274C')

        # Removes a set amount of coins from a user
        elif command.lower() == 'remove' and len(args) == 2:
            user_id = args[0].replace('<@', '').replace('!','').replace('>', '')
            if self.c.execute('''SELECT 1 FROM users WHERE id=?''', (user_id,)).fetchone():
                self.c.execute('''UPDATE users SET xp = xp-? WHERE id=?''', (args[1], user_id))
                self.connection.commit()
                return await ctx.message.add_reaction('\U00002705')
            else:
                return await ctx.message.add_reaction('\U0000274C')

        # Sets a users balance to a certain amount
        elif command.lower() == 'set' and len(args) == 2:
            user_id = args[0].replace('<@', '').replace('!','').replace('>', '')
            if self.c.execute('''SELECT 1 FROM users WHERE id=?''', (user_id,)).fetchone():
                self.c.execute('''UPDATE users SET xp=? WHERE id=?''', (args[1], user_id))
                self.connection.commit()
                return await ctx.message.add_reaction('\U00002705')
            else:
                return await ctx.message.add_reaction('\U0000274C')

        # Resets a users balance to 0
        elif command.lower() == 'reset' and len(args) == 1:
            user_id = args[0].replace('<@', '').replace('!','').replace('>', '')
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
            print(str(error))
            return await ctx.message.add_reaction('\U0000274C')
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.message.add_reaction('\U0001F552')
        else:
            raise error


def setup(bot):
    bot.add_cog(Currency(bot))
