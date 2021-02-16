import discord

from discord.ext import commands


class General(commands.Cog, name="General Commands"):
  def __init__(self, bot):
        self.bot = bot
        
  #@commands.command(name='invite')
  #async def invite(self, ctx): #Pulls up an invite link.
      #await ctx.message.channel.send("<https://cheddydev.com/discord>")

  @commands.command(name='report')
  async def report(self, ctx): #Helps a user report.
      await ctx.message.delete()
      await ctx.message.channel.send("Need to report someone? Open a modmail with !dm")

  @commands.command(name='help')
  async def help(self, ctx): #Help command
      desc = 'Thanks for using the Trivskins Trading Bot, coded and created by cheddy#7744. Please contact him if you have any issues. '
      features1 = 'This bot has many features, please take a look at the commands available to you below.'
      commands1 = '**!dm** *Report someone/get server support.*\n**!value "Steam Profile Link"** *Gives the CS:GO inventory value of a steam profile.* \n**!pc "Weapon" "Skin" "Wear"** *Price check a skin.*\n**!invite** *Get the Discord invite link.* \n**!support** *Help support the hosting of this bot.***\n**!help** *Pull up this help menu.*'
      embed = discord.Embed(title="Trivskins Trading Bot Help", description=desc, url='https://cheddydev.com/', color=0X2C3675)
      embed.add_field(name="Features", value=features1, inline=False)
      embed.add_field(name="Commands", value=commands1, inline=False) 
      await ctx.message.channel.send(embed=embed)

  @commands.command(name='support')
  async def support(self, ctx): #Supporters command.
      desc = 'Coding this bot and making the website is free, unfortunatly hosting them is not. Every **$10** donated keeps the bot and the website live for another month.'
      supporters = 'Thank you to anyone who supports the bot, the website, and this server. Donating any amount will get your name below, a royal purple chat role, and future supporter only betas and bot features! \n\n**Argarest**\n**ÅRRØ**'
      paypal = 'Please visit **https://cheddydev.com/support/** to see all the different ways to support the server.'
      embed = discord.Embed(title="Support!", description=desc, url='https://www.paypal.me/cheddy', color=0Xac27fd)
      embed.add_field(name="Ways to Support", value=paypal, inline=False)
      embed.add_field(name="Supporters", value=supporters, inline=False)
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
