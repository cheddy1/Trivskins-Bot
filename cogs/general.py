# This cog provides some general usage commands. At some point, I'd like
# to add a functionality that allows to create more commands from inside
# the server itself and stores them.

import discord
from discord.ext import commands

# Class declaration 
class General(commands.Cog, name="General Commands"):
  def __init__(self, bot):
        self.bot = bot
        
  # Pulls up an invite link
  @commands.command(name='invite')
  async def invite(self, ctx): 
      await ctx.message.channel.send("https://discord.gg/NfpThYWgRt")

  #Alerts a user about modmail
  @commands.command(name='modmail')
  async def modmail(self, ctx): 
      await ctx.message.delete()
      mention = ctx.message.content.replace('!modmail','')
      print(mention)
      await ctx.message.channel.send('Need to report someone, provide feedback, or get support, '+mention+'? Open a modmail with **!dm**')

  # General help command
  @commands.command(name='help')
  async def help(self, ctx): 
      desc = 'Thanks for using the Trivskins Trading Bot, coded and created by cheddy#7744. Please contact him if you have any issues. '
      features1 = 'This bot has many features, please take a look at the commands available to you below.'
      commands1 = '**!dm** *Report someone/get server support.*\n**!value "Steam Profile Link"** *Gives the CS:GO inventory value of a steam profile.* \n**!pc "Weapon" "Skin" "Wear"** *Price check a skin.*\n**!invite** *Get the Discord invite link.* \n**!support** *Help support the hosting of this bot.*\n**!help** *Pull up this help menu.*'
      embed = discord.Embed(title="Trivskins Trading Bot Help", description=desc, url='https://cheddydev.com/', color=0X2C3675)
      embed.add_field(name="Features", value=features1, inline=False)
      embed.add_field(name="Commands", value=commands1, inline=False) 
      await ctx.message.channel.send(embed=embed)

  # Recognizes supporters. At some point, would like to add an ability to add
  # supporters from the server.
  @commands.command(name='support')
  async def support(self, ctx): 
      desc = 'Coding this bot and making the website is free, unfortunatly hosting them is not. Every **$10** donated keeps the bot and the website live for another month.'
      supporters = 'Thank you to anyone who supports the bot, the website, and this server. Donating any amount will get your name below, a royal purple chat role, and future supporter only betas and bot features! \n\n**Argarest**\n**ÅRRØ**'
      paypal = 'Please visit **https://cheddydev.com/support/** to see all the different ways to support the server.'
      embed = discord.Embed(title="Support!", description=desc, url='https://www.paypal.me/cheddy', color=0Xac27fd)
      embed.add_field(name="Ways to Support", value=paypal, inline=False)
      embed.add_field(name="Supporters", value=supporters, inline=False)
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
