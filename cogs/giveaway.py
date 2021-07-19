import discord
import asyncio
import random
import sqlite3
import time
from discord.ext import tasks, commands
from datetime import datetime

connection = sqlite3.connect('Trivskins.db')
cursor = connection.cursor()
giveaway_channel = 0 
giveaway_blacklist = []
guild_id = 0 


class Giveaway(commands.Cog, name="Giveaways"):
    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect("Trivskins.db")
        self.c = self.connection.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS giveaways (name text PRIMARY KEY, prize text NOT NULL, end_time integer NOT NULL, winners integer NOT NULL, ticket_cost integer NOT NULL, ticket_max integer NOT NULL)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS entries (name text NOT NULL, id INTEGER NOT NULL, tickets INTEGER NOT NULL)''')


    @commands.Cog.listener()
    async def on_ready(self):
        self.giveaway_update.start()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx, checker, *args):
        if checker.lower() == 'create':
            if not args:
                return await ctx.message.channel.send("To create a giveaway, you must provide a name: `!giveaway create (name)`")
            giveaway_name = ' '.join(args)
            self.c.execute('''SELECT name FROM giveaways WHERE name=?''', (giveaway_name,))
            if self.c.fetchone():
                return await ctx.message.channel.send("A giveaway already exists with this name.")
            else:
                try:
                    await ctx.message.channel.send("Creating a giveaway! What do you want to give away?")
                    prize = await self.bot.wait_for('message', check=lambda message: message.channel == ctx.message.channel and message.author.id != self.bot.user.id, timeout=60)
                    await ctx.message.channel.send("Okay, the prize will be " + prize.content + ". How long should this last (in hours)?")
                    duration = await self.bot.wait_for('message', check=lambda message: message.channel == ctx.message.channel and message.author.id != self.bot.user.id, timeout=60)
                    await ctx.message.channel.send("Okay, the giveaway will be open for " + duration.content + " hours. How many winners should there be?")
                    winners = await self.bot.wait_for('message', check=lambda message: message.channel == ctx.message.channel and message.author.id != self.bot.user, timeout=60)
                    await ctx.message.channel.send("Okay, there will be " + winners.content + " winners. How much should each ticket cost?" )
                    ticket_cost = await self.bot.wait_for('message', check=lambda message: message.channel == ctx.message.channel and message.author.id != self.bot.user.id, timeout=60)
                    await ctx.message.channel.send("Okay, each ticket will cost " + ticket_cost.content + " coins. What is the max number of tickets a user can buy?" )
                    ticket_max = await self.bot.wait_for('message', check=lambda message: message.channel == ctx.message.channel and message.author.id != self.bot.user.id, timeout=60)
                except asyncio.TimeoutError:
                    return await ctx.message.channel.send("Timed out!")
                end_time = time.time() + float(duration.content)*3600
                end_datetime = datetime.fromtimestamp(int(end_time)).strftime("%A, %B %d, at %I:%M") + ' CST'
                embed_desc = "Prize: **" + prize.content + "**\nEnd Time: **" + end_datetime + "**\nNumber of Winners: **" + winners.content + "**\nTicket Cost: **" + ticket_cost.content + "** coins\nTicket Limit: **" + ticket_max.content + "** tickets"
                embed = discord.Embed(title="🎉 "+giveaway_name+" 🎉", description=embed_desc, color=0XFFFF00)
                embed.set_footer(text='Enter this giveaway using !buy ticket (# of tickets) '+ giveaway_name)
                await ctx.guild.get_channel(giveaway_channel).send(embed=embed)
                self.c.execute('''INSERT OR IGNORE INTO giveaways VALUES (?, ?, ?, ?, ?, ?)''', (giveaway_name, prize.content, end_time, winners.content, ticket_cost.content, ticket_max.content))
                self.connection.commit()
                await ctx.message.channel.send("Okay, I made a giveaway with these details;\nName: " + giveaway_name + "\nPrize: " + prize.content + "\nDuration: " + duration.content + " hours\nWinners: " + winners.content + "\nTicket Cost: " + ticket_cost.content + "\nMax Tickets: " + ticket_max.content)


    @tasks.loop(seconds=60)
    async def giveaway_update(self):
        end_times = self.c.execute('''SELECT name, end_time FROM giveaways''').fetchall()
        if end_times:
            for timestr in end_times:
                if int(time.time()) > timestr[1]:
                    num_winners = self.c.execute('''SELECT winners FROM giveaways WHERE name=?''', (timestr[0],)).fetchone()
                    entries = self.c.execute('''SELECT id, tickets FROM entries WHERE name=?''', (timestr[0],)).fetchall()
                    guild = self.bot.get_guild(guild_id)
                    if not entries:
                        return await guild.get_channel(giveaway_channel).send('No one entered in \"'+ timestr[0] + '\"...')
                    total_entry_list = []
                    total_tickets = 0
                    for user in entries:
                        user_id = user[0]
                        tickets = user[1]
                        for i in range(tickets):
                            total_entry_list.append(user_id)
                            total_tickets += 1
                    if num_winners[0] == 1:
                        while True:
                            winning_index = random.randint(0, total_tickets - 1)
                            winner_id = total_entry_list[winning_index]
                            if winner_id not in giveaway_blacklist:
                                winner_tickets = self.c.execute('''SELECT tickets FROM entries WHERE name=? AND id=?''', (timestr[0], winner_id)).fetchone()
                                chance_winning = round(float(winner_tickets[0] / total_tickets) * 100, 2)
                                winner_str = '🎉 Congrats <@' + str(winner_id) + '> , you are the winner of \"**' + timestr[0] + '**\"!! 🎉 \nThey had a **' + str(chance_winning) + '%** chance of winning!'
                                break
                    else:
                        winner_list = []
                        winners_str = ''
                        count = 1
                        for i in range(num_winners[0]):
                            while True:
                                winning_index = random.randint(0, total_tickets - 1)
                                winner_id = total_entry_list[winning_index]
                                if winner_id not in winner_list and winner_id not in giveaway_blacklist:
                                    winner_list.append(winner_id)
                                    break
                        for winner_id in winner_list:
                            winner_tickets = self.c.execute('''SELECT tickets FROM entries WHERE name=? AND id=?''', (timestr[0], winner_id)).fetchone()
                            chance_winning = round(float(winner_tickets[0] / total_tickets) * 100, 2)
                            winners_str += '\n' + str(count) + '. <@' + str(winner_id) + '> *(**' + str(chance_winning) + '%** chance of winning)*'
                            count += 1
                        winner_str = '🎉 Congrats to our following winners! 🎉' + winners_str + '\nY\'all have won \"**' + timestr[0] + '**\"!! 🎉'
                    await guild.get_channel(giveaway_channel).send(winner_str)
                    self.c.execute('''DELETE FROM giveaways WHERE name=?''', (timestr[0],))
                    self.connection.commit()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearentries(self, ctx, *args):
        giveaway_name = ' '.join(args)
        giveaway_existed = self.c.execute('''SELECT * FROM entries WHERE name=?''', (giveaway_name,)).fetchone()
        if giveaway_existed:
            self.c.execute('''DELETE FROM entries WHERE name=?''', (giveaway_name,))
            self.connection.commit()
            return await ctx.message.add_reaction('\U00002705')
        else:
            return await ctx.message.add_reaction('\U0000274C')


def setup(bot):
    bot.add_cog(Giveaway(bot))
