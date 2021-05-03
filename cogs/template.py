# This cog forces users who are posting in trading channels to follow
# predetermined templates to keep all trading ads consistant and neat.
# It also removes any ads with certain words not allowed by the server.

from discord.ext import commands
import re

# Channel IDs for the bot to check for/use
tradelogging = 
lowHighChannels = [,]
steamChannelList = [,,,,,]
RLChannelList = [,,,]
tradetemplate = ''

# Class declaration 
class Template(commands.Cog, name="Ad Template Checker"):
  def __init__(self, bot):
        self.bot = bot

  # React on any message sent
  @commands.Cog.listener()
  async def on_message(self, ctx):

    # Ignore if in a dm message
    guild = ctx.guild
    if guild == None:
        return
    
    else:

        # Define logging channel and banned list of words
        logging = guild.get_channel(tradelogging)
        banned_list = ['cash','paypal','steam card','gift card', 'bitcoin','btc','crypto','steam gift card','alipay','bank transfer','eth','qq','dollar','usd','euro']

        # Makes sure the user is not spamming the channel by checking who was the last one to post
        async def checkSpam():
            fetchID = await ctx.channel.history(limit = 2).flatten()

            if (fetchID[1].author != ctx.author):

                if ctx.author.bot:
                    pass

                else:
                    await ctx.delete()
                    await logging.send(ctx.author.mention+", please wait until someone else posts an ad before posting yours again. Please refer to <#"+tradetemplate+"> for our rules.\n")
                    return(True)
            else:
                return(False)

        # Make sure a user hasn't used any of the banned words in their ad
        async def checkBannedWords():
            wordList = re.findall(r"(?=\b("+'|'.join(banned_list)+r")\b)", ctx.content.lower())
            if wordList:

                if ctx.author.bot:
                    pass

                else:
                    word = ', '.join(wordList)
                    await logging.send("Sorry "+ctx.author.mention+", but your ad included banned word(s) or phrase(s). You said **"+word+ "** which is currently not allowed according to our rules. \nPlease refer to the list of banned words and phrases in <#"+tradetemplate+"> before posting again.\n")
                    await ctx.delete()
                    return(True)
            else:
                return(False)

        # Steam based game channels
        if (ctx.channel.id in steamChannelList):

            if (await checkSpam()):
                pass

            else: 
                
                # Make sure the user's ad follows the template
                if ("[H]" not in ctx.content) or ("[W]" not in ctx.content) or (("steamcommunity.com/tradeoffer" not in ctx.content) and ("[TL]" not in ctx.content)):

                    if ctx.author.bot:
                        pass

                    else:
                        await logging.send("Sorry "+ctx.author.mention+", but your trade ad didn't follow our required template, and therefore deleted. Please refer to <#"+tradetemplate+"> before posting again.\n")

                    await ctx.delete()
                
                elif (await checkBannedWords()):
                    pass
                
                else:

                    # If the ad passes all other checks, make sure that the ad does not have a knife in the incorrect channel
                    if (ctx.channel.id in lowHighChannels):
                        ad = ctx.content.lower()

                        if (ad.find('knife') < ad.find('[w]') and ad.find('knife') > 0) or (ad.find('daggers') < ad.find('[w]') and ad.find('daggers') > 0) or (ad.find('bayonet') < ad.find('[w]') and ad.find('bayonet') > 0) or (ad.find('karambit') < ad.find('[w]') and ad.find('karambit') > 0) or (ad.find('glove') < ad.find('[w]') and ad.find('glove') > 0):
                            await logging.send("Bad puppy, "+ctx.author.mention+"! Looks like you had a knife/glove in your **[H]** block. Please post the knife/glove as a separate ad in <#556875284574371871>.\n")
                            await ctx.delete()
        
        # Rocket League Channels
        elif (ctx.channel.id in RLChannelList):

            if (await checkSpam()):
                pass

            else:
                
                # Same template checker, just without the trade link
                if ("[H]" not in ctx.content) or ("[W]" not in ctx.content):

                    if ctx.author.bot:
                        pass

                    else:
                        await logging.send("Sorry "+ctx.author.mention+", but your trade ad didn't follow our required template, and therefore deleted. Please refer to <#"+tradetemplate+"> before posting again.\n")
                    await ctx.delete()
                    
                else:
                    await checkBannedWords()

def setup(bot):
    bot.add_cog(Template(bot))
