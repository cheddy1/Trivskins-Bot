from discord.ext import commands

tradelogging = 
tradelow = 
tradehigh = 
tradeknife = 
tradetemplate = ''

class Template(commands.Cog, name="Template Follower"):
  def __init__(self, bot):
        self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, ctx):
    guild = ctx.guild
    if guild == None:
        return
    else:
        logging = guild.get_channel(tradelogging) #Trade logging
        banned_list = ['cash','paypal','steam card','gift card', 'bitcoin','btc','crypto','steam gift card','Cash','Paypal','PayPal','Steam card','Steam Card','Gift card','Gift Card', 'Bitcoin','BitCoin','BTC','Crypto','Steam gift card']
        if (ctx.channel.id == tradelow) or (ctx.channel.id == tradehigh) or (ctx.channel.id == tradeknife): #Trade ad channels
            if ("[H]" not in ctx.content) or ("[W]" not in ctx.content) or (("steamcommunity.com/tradeoffer" not in ctx.content) and ("[TL]" not in ctx.content)):
                if ctx.author.bot:
                    pass
                else:
                    await logging.send("Sorry "+ctx.author.mention+", but your trade ad didn't follow our required template, and therefore deleted. Please refer to <#"+tradetemplate+"> before posting again.\n")
                await ctx.delete()
            elif [ele for ele in banned_list if(ele in ctx.content)] :
                if ctx.author.bot:
                    pass
                else:
                    await logging.send("Sorry "+ctx.author.mention+", but your ad included banned word(s) or phrase(s). Please refer to the list of banned words and phrases in <#"+tradetemplate+"> before posting again.\n")
                await ctx.delete()
            else:
              pass
        else:
          pass
def setup(bot):
    bot.add_cog(Template(bot))
