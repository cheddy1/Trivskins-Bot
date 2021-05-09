import discord  
import aiohttp
from discord.ext import commands
import json
import difflib
import asyncio

listOfItems = []
allSkinsData = {}
priceCheckChannel = 

class priceCheck(commands.Cog, name="Price check command"):
  def __init__(self, bot):
      self.bot = bot
  
  # Runs when the bot is first started up
  @commands.Cog.listener()
  async def on_ready(self): 
      channel = self.bot.get_channel(priceCheckChannel)
      
      # Refresh the skin list on startup and every 24 hours
      while True:
          global listOfItems
          global allSkinsData
          
          async with aiohttp.ClientSession() as session:
              async with session.get('http://csgobackpack.net/api/GetItemsList/v2/') as resp:
                  resp = await resp.text()
                  tempJson = json.loads(resp)
                  
                  if tempJson['success'] == True:
                      allSkinsData = json.loads(resp)
                      listOfItems = list(allSkinsData['items_list'].keys())
                      await channel.send("CS:GO skins and prices refreshed.")
                      await asyncio.sleep(86400)
                  
                  else:
                      await channel.send("Could not reload the item list. Is CSGO Backpack down?")
                      await asyncio.sleep(86400)
              
  # CSGO skin market price skin checker command
  @commands.command(name='pc')
  async def pc(self, ctx): 
    async with ctx.typing():
      skinName = ctx.message.content.replace(ctx.message.content[0:3], '')
      
      # If the user doesn't input a skin, tell them
      if skinName == "":
          await ctx.send('!pc cannot be empty, '+ ctx.message.author.mention+'. Type !pc help to get started!')
      
      else:
          
          # This should never happen, but if the skin list is empty, it needs to be reloaded
          if not listOfItems:
              await ctx.send("Please wait for the list of skins to load!")
          
          else:
              rawSkinName = difflib.get_close_matches(skinName.title(), listOfItems,1,.4)
              
              # This happens if the user does not input a skin close enough to the correct one
              if not rawSkinName:
                  await ctx.send("No results. Please try again or ping <@217440011451105280> if you have any issues.")
              
              # Get the skin data and print it
              else:
                  rawSkinName = rawSkinName[0]
                  requestedSkinData = allSkinsData['items_list'][rawSkinName]
                  color = int(hex(int(requestedSkinData['rarity_color'], 16)),16)
                  requestedSkinDataPrice = requestedSkinData['price']['30_days']
                  averagePrice = str(requestedSkinDataPrice['average'])
                  lowestPrice = str(requestedSkinDataPrice['lowest_price'])
                  highestPrice = str(requestedSkinDataPrice['highest_price'])
                  amountSold = str(requestedSkinDataPrice['sold'])
                  skinIcon = "http://cdn.steamcommunity.com/economy/image/"+str(requestedSkinData['icon_url']+"/")
                  steamLink= ('https://steamcommunity.com/market/listings/730/'+rawSkinName.replace(')','%29')).replace(' ','%20')
                  bitskinsLink= ('https://bitskins.com/?app_id=730&market_hash_name='+rawSkinName.replace(')','%29')).replace(' ','%20')
                  desc='The average price for \n' +'**'+rawSkinName+'** is: **$'+averagePrice+'**\n\nAmount sold: **'+amountSold+'**\nLowest price sold for: **$'+lowestPrice+'**\nHighest price sold for: **$'+highestPrice+'**'
                  embed = discord.Embed(title="Price Check", description=desc, url=skinIcon,  color=color)
                  links = "[Steam Market]("+steamLink+")\n[Bitskins]("+bitskinsLink+")\n_ _"
                  embed.add_field(name="Links", value=links, inline=False)
                  embed.set_thumbnail(url=skinIcon)
                  embed.set_footer(text="All data is from the steam marketplace from the past 30 days", icon_url="https://cdn.discordapp.com/avatars/217440011451105280/7752b9953c981fe9b072dd0949e956f4.png?size=128")
                  await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(priceCheck(bot))
