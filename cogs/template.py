# This cog forces users who are posting in trading channels to follow
# predetermined templates to keep all trading ads consistant and neat.
# It also removes any ads with certain words not allowed by the server.

from discord.ext import commands
import re

# Channel IDs for the bot to refer to
tradelogging = 
tradelow = 
tradehigh = 
tradeknife = 
tradetemplate = ''

# Class declaration 
class Template(commands.Cog, name="Forced Template"):
  def __init__(self, bot):
        self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, ctx):
    # Ignore if in a dm message
    guild = ctx.guild
    
    if guild == None:
        return
    
    else:
        # Define logging channel and banned list of words
        logging = guild.get_channel(tradelogging)
        banned_list = ['cash','paypal','steam card','gift card', 'bitcoin','btc','crypto','steam gift card','tf2','team fortress','alipay','bank transfer','eth','qq']
        
        # Trade ad channels
        if (ctx.channel.id == tradelow) or (ctx.channel.id == tradehigh) or (ctx.channel.id == tradeknife):
            
            # Ad tempplate checker
            if ("[H]" not in ctx.content) or ("[W]" not in ctx.content) or (("steamcommunity.com/tradeoffer" not in ctx.content) and ("[TL]" not in ctx.content)):
                if ctx.author.bot:
                    pass
                else:
                    await logging.send("Sorry "+ctx.author.mention+", but your trade ad didn't follow our required template, and therefore deleted. Please refer to <#"+tradetemplate+"> before posting again.\n")
                await ctx.delete()
            
            # Banned word checker
            elif re.compile('|'.join(banned_list),re.IGNORECASE).search(ctx.content):
                if ctx.author.bot:
                    pass
                else:
                    words = re.compile('|'.join(banned_list),re.IGNORECASE).findall(ctx.content)
                    word = ', '.join(words)
                    await logging.send("Sorry "+ctx.author.mention+", but your ad included banned word(s) or phrase(s). You said **"+word+ "** which is currently not allowed according to our rules. \nPlease refer to the list of banned words and phrases in <#"+tradetemplate+"> before posting again.\n")
                    await ctx.delete()
            
            # If the ad passes all other checks, make sure that the ad does not have a knife in the incorrect channel
            elif (ctx.channel.id == tradelow) or (ctx.channel.id == tradehigh):
                ad = ctx.content.lower()
                if (ad.find('knife') < ad.find('[w]') and ad.find('knife') > 0) or (ad.find('daggers') < ad.find('[w]') and ad.find('daggers') > 0) or (ad.find('bayonet') < ad.find('[w]') and ad.find('bayonet') > 0) or (ad.find('karambit') < ad.find('[w]') and ad.find('karambit') > 0):
                    await logging.send("Bad puppy, "+ctx.author.mention+"! Looks like you had a knife in your **[H]** block. Please post the knife as a separate ad in <#"+str(tradeknife)+">.\n")
                    await ctx.delete()
            else:
              pass
        else:
          pass
def setup(bot):
    bot.add_cog(Template(bot))
