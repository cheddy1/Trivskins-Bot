import discord
import aiohttp
import ast
from discord.ext import commands

# Steam API is required to get certain idetifiers from a users url
steamapi = '876F8F0BCC5942F76AB49B8622D730A1'
# CSGO backpack api, 
key = 'f85aae2295yh2xwg'

class Value(commands.Cog, name="Inventory Value Commands"):
  def __init__(self, bot):
        self.bot = bot
  
  @commands.command(name='value')
  async def value(self, ctx):

      # Get the appropriate color for the embed
      def getColor(moneyValue):
        if moneyValue < 1:
            color = 0XFFFFFF                              
        elif 1 < moneyValue < 24.99:
            color = 0Xe9fdff                       
        elif 25 < moneyValue <49.99:
            color = 0Xd0fbff                                  
        elif 50 < moneyValue <99.99:
            color = 0X9df7ff                            
        elif 100 < moneyValue <199.99:
            color = 0X64effb                                   
        elif 200 < moneyValue <499.99:
            color = 0X42e9f7                                  
        elif 500 < moneyValue <999.99:
            color = 0X1ce8f9                                   
        elif 1000 < moneyValue <4999.99:
            color = 0X00e4f7                                  
        elif 5000 < moneyValue <9999.99:
            color = 0X3bc2cd                                  
        elif 10000 < moneyValue:
            color = 0X03b3c2   
        return color

      # Get just the profile url from the command
      remove = ctx.message.content
      remove1 = remove[0:7]
      profile = remove.replace(remove1, '')
      
      async with ctx.typing():
          try:

              # Check if user has a vanity url, if yes, return the required steam ID
              if '/profiles/' in profile:
                  if 'https://steamcommunity.com/profiles/' in profile:
                      removalURL = 'https://steamcommunity.com/profiles/'
                      steamID = profile.replace(removalURL,'').replace('/','')
                  else:
                      removalURL = 'http://steamcommunity.com/profiles/'
                      steamID = profile.replace(removalURL,'').replace('/','')
              if '/id/' in profile:
                  if 'https://steamcommunity.com/id/' in profile:
                      removalURL = 'https://steamcommunity.com/id/'
                      vanity = profile.replace(removalURL,'').replace('/','')
                  else:
                      removalURL = 'http://steamcommunity.com/id/'
                      vanity = profile.replace(removalURL,'').replace('/','')
                  async with aiohttp.ClientSession() as session:
                      async with session.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key='+steamapi+'&vanityurl='+vanity) as resp:
                          id64 = await resp.text()
                          if ':42' in id64:
                              steamID = '0'
                          else:
                              removeLH = '{\"response\":{\"steamid\":\"'
                              removeRH = '\",\"success\":1}}'
                              steamID = id64.replace(removeLH,'').replace(removeRH,'')

              # Gets all the available public data from a steam profile
              async with aiohttp.ClientSession() as session:
                  async with session.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+steamapi+'&steamids='+steamID) as resp:
                      resp = await resp.text()
                      getData = resp.replace(' ','⠀').replace(',',' ').split()
                      nameIndex = [i for i, elem in enumerate(getData) if 'personaname' in elem]
                      profileName = getData[int(''.join([str(i) for i in nameIndex]))].replace('\"personaname\":\"','').replace('\"','').replace('\'','')
                      avatarIndex = [i for i, elem in enumerate(getData) if 'avatarfull' in elem]
                      avatarLink = getData[int(''.join([str(i) for i in avatarIndex]))].replace('\"avatarfull\":\"','')

                      # Gets the users CSGO inventory value using the CSGO Backpack API
                      async with aiohttp.ClientSession() as session:
                        async with session.get('http://csgobackpack.net/api/GetInventoryValue/?id='+steamID+"&key="+key) as resp:
                            csgoData = await resp.text()
                            if '\"true\"' in csgoData:
                                csgoData = ast.literal_eval(csgoData)
                                moneyValue = float(csgoData['value'])
                                itemValue = csgoData['items']
                                embedColor = getColor(moneyValue)
                                await ctx.message.delete()
                                user = ctx.message.guild.get_member(ctx.message.author.id)
                                pfp = user.avatar_url
                                desc = ctx.message.author.mention + ', here you go. \n\nSteam Name: **'+profileName+'** \nCS:GO inventory value of **'+itemValue+'** items: **```py\n$'+str(moneyValue)+' USD```**\n[Profile Link]('+profile+')\n'
                                embed = discord.Embed(title="CS:GO Inventory value", description=desc, url='https://cheddydev.com/', color=embedColor)
                                embed.set_thumbnail(url=avatarLink)
                                embed.set_footer(text="Inventory value based on current Steam market prices.", icon_url=pfp)
                                await ctx.message.channel.send(embed=embed)
                            if '\"false\"' in csgoData:
                                await ctx.message.delete()
                                await ctx.message.channel.send('Sorry '+ctx.message.author.mention+', CS:GO Backpack didn\'t return any data on <'+profile+'>. \nMake sure the steam inventory isn\'t private, or that <https://steamstat.us/> isn\'t down, and try again.')  
          except:
              await ctx.message.delete()
              if not profile:
                  await ctx.message.channel.send(ctx.message.author.mention+', you\'re missing a profile link!', delete_after=20.0)
              else:
                  await ctx.message.channel.send('Sorry '+ctx.message.author.mention+', there was an error getting <'+profile+'>. Please make sure that this is a valid profile link, and if it is, please ping @cheddy.',delete_after=30.0)
                  
def setup(bot):
    bot.add_cog(Value(bot))
