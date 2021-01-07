from discord.ext import commands
import re

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
        banned_list = ['cash','paypal','steam card','gift card', 'bitcoin','btc','crypto','steam gift card','tf2','team fortress','alipay','bank transfer','eth','qq']
        if (ctx.channel.id == tradelow) or (ctx.channel.id == tradehigh) or (ctx.channel.id == tradeknife): #Trade ad channels
            if ("[H]" not in ctx.content) or ("[W]" not in ctx.content) or (("steamcommunity.com/tradeoffer" not in ctx.content) and ("[TL]" not in ctx.content)):
                if ctx.author.bot:
                    pass
                else:
                    await logging.send("Sorry "+ctx.author.mention+", but your trade ad didn't follow our required template, and therefore deleted. Please refer to <#"+tradetemplate+"> before posting again.\n")
                await ctx.delete()
            elif re.compile('|'.join(banned_list),re.IGNORECASE).search(ctx.content):
                if ctx.author.bot:
                    pass
                else:
                    words = re.compile('|'.join(banned_list),re.IGNORECASE).findall(ctx.content)
                    word = ', '.join(words)
                    await logging.send("Sorry "+ctx.author.mention+", but your ad included banned word(s) or phrase(s). You said **"+word+ "** which is currently not allowed according to our rules. \nPlease refer to the list of banned words and phrases in <#"+tradetemplate+"> before posting again.\n")
                    await ctx.delete()
            elif (ctx.channel.id == tradelow) or (ctx.channel.id == tradehigh):
                if (ctx.content.find('knife') < ctx.content.find('[W]') and ctx.content.find('knife') > 0) or (ctx.content.find('Knife') < ctx.content.find('[W]') and ctx.content.find('Knife') > 0):
                    await logging.send("Bad puppy, "+ctx.author.mention+"! Looks like you had a knife in your **[H]** block. Please post the knife as a separate ad in <#"+str(tradeknife)+">.\n")
                    await ctx.delete()
            else:
              pass
        else:
          pass
def setup(bot):
    bot.add_cog(Template(bot))
