import discord
import requests
from discord.ext import commands

steamapi = '' #steam api
key = '' CSGO backpack api
class Value(commands.Cog, name="Inventory Value Commands"):
  def __init__(self, bot):
        self.bot = bot

  
  @commands.command(name='value')
  async def value(self, ctx): #Checks steam ID, gets the csgo inventory value of any steam profile.
    remove = ctx.message.content
    remove1 = remove[0:7]
    profile = remove.replace(remove1, '')
    
    async with ctx.typing():
        try:
            global userid
            global money
            if '/profiles/' in profile:
                if 'https://steamcommunity.com/profiles/' in profile:
                    removal = 'https://steamcommunity.com/profiles/'
                    vanity1 = profile.replace(removal,'')
                    vanity = vanity1.replace('/','')
                    steamid = vanity
                else:
                    removal2 = 'http://steamcommunity.com/profiles/'
                    vanity2 = profile.replace(removal2,'')
                    vanity = vanity2.replace('/','')
                    steamid = vanity
            if '/id/' in profile:
                if 'https://steamcommunity.com/id/' in profile:
                    removal1 = 'https://steamcommunity.com/id/'
                    vanity1 = profile.replace(removal1,'')
                    vanity = vanity1.replace('/','')
                else:
                    removal2 = 'http://steamcommunity.com/id/'
                    vanity2 = profile.replace(removal2,'')
                    vanity = vanity2.replace('/','')
                steamresp = requests.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key='+steamapi+'&vanityurl='+vanity) #You'll need to set your own Steam API key here, or else it won't work.
                #print('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=9AA3367B9ACDC3C6F4ED7E9AB3B75822&vanityurl='+vanity)
                id64 = steamresp.text
                if ':42' in id64:
                    steamid = '0'
                else:
                    remove = '{\"response\":{\"steamid\":\"'
                    remove2 = '\",\"success\":1}}'
                    steamid1 = id64.replace(remove,'')
                    steamid = steamid1.replace(remove2,'')
            getdata1 = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+steamapi+'&steamids='+steamid) #You'll need to set your own Steam API key here, or else it won't work.
            getdata = getdata1.text
            getdata2 = getdata.replace(' ','⠀')
            getdata3 = getdata2.replace(',',' ')
            getdata4 = getdata3.split()
            nameindex1 = [i for i, elem in enumerate(getdata4) if 'personaname' in elem]
            nameindex2 = ''.join([str(i) for i in nameindex1])
            nameindex = int(nameindex2)
            name1 = getdata4[nameindex]
            name2 = name1.replace('\"personaname\":\"','')
            name3 = name2.replace('\"','')
            name = name3.replace('\'','')
            avatarindex1 = [i for i, elem in enumerate(getdata4) if 'avatarfull' in elem]
            avatarindex2 = ''.join([str(i) for i in avatarindex1])
            avatarindex = int(avatarindex2)
            avatarlink1 = getdata4[avatarindex]
            avatarlink = avatarlink1.replace('\"avatarfull\":\"','')
            resp = requests.get('http://csgobackpack.net/api/GetInventoryValue/?id='+steamid+"&key="+key) 
            data=resp.text
            if '\"true\"' in data:
                moneyxd = data[27:34]
                money2 = moneyxd.replace(",", "")
                money3 = money2.replace("it", "")
                money4 = money3.replace("\"", "")
                money5 = money4.replace("i", "")
                money6 = money5.replace("t", "")
                money = money6.replace(",", "")
                money1 = float(money)
                if not money:
                    await ctx.message.delete()
                    await ctx.message.channel.send('Sorry '+ctx.message.author.mention+', this steam profile is not valid. If you think it should be, please @ cheddy.',delete_after=10.0)
                else:
                    if money1 < 1:
                        color2=0XFFFFFF                              
                    if 1 < money1 < 24.99:
                        color2=0Xe9fdff                       
                    if 25 < money1 <49.99:
                        color2=0Xd0fbff                                  
                    if 50 < money1 <99.99:
                      color2=0X9df7ff                            
                    if 100 < money1 <199.99:
                        color2=0X64effb                                   
                    if 200 < money1 <499.99:
                        color2=0X42e9f7                                  
                    if 500 < money1 <999.99:
                        color2=0X1ce8f9                                   
                    if 1000 < money1 <4999.99:
                        color2=0X00e4f7                                  
                    if 5000 < money1 <9999.99:
                        color2=0X3bc2cd                                  
                    if 10000 < money1:
                        color2=0X03b3c2   
                    await ctx.message.delete()
                    user = ctx.message.guild.get_member(ctx.message.author.id)
                    pfp = user.avatar_url
                    desc = ctx.message.author.mention + ', here you go. \n\nSteam Name: **'+name+'** \nCS:GO Inventory Value: **```py\n$'+money+' USD```**\n[Profile Link]('+profile+')\n'
                    embed = discord.Embed(title="CS:GO Inventory Value", description=desc, url='https://cheddydev.com/', color=color2)
                    embed.set_thumbnail(url=avatarlink)
                    embed.set_footer(text="Inventory value based on current Steam market prices.", icon_url=pfp)
                    await ctx.message.channel.send(embed=embed)
            if '\"false\"' in data:
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
