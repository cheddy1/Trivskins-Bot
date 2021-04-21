import discord
import aiohttp
import datetime
import ast
from discord.ext import commands

screenshotchannel = 569979062513041408

class screenshotTwo(commands.Cog, name="Screenshot"):
  def __init__(self, bot):
      self.bot = bot
    
  @commands.Cog.listener()
  async def on_message(self, ctx):
    guild = ctx.guild
    if guild == None:
        return
    else:
      
      # Gets the color of the quality for the embed based off of CS:GO skin colors
      async def getColor(rarityName):
          if rarityName == 'Consumer Grade':
              color1 = 0XC2C2C2
          elif rarityName == 'Industrial':
              color1 = 0X77A5FF
          elif rarityName == 'Mil-Spec Grade':
              color1 = 0X3C66DA
          elif rarityName == 'Restricted':
              color1 = 0X893AE7
          elif rarityName == 'Classified':
              color1 = 0XD437D2
          elif rarityName == 'Covert':
              color1 = 0XE81E02
          else:
              color1 = 0XFFD700
          return color1
      
      # Gets the needed data and prints the screenshot embed
      async def getScreenshot():
          csgoFloatAPI = "https://api.csgofloat.com/?url="
          screenshotWebsite = "https://csgo.gallery/" 
          inspectURL = ctx.content
          screenshotURL = screenshotWebsite+inspectURL
          csgoFloatRawData = csgoFloatAPI+inspectURL

          # Gets all the needed data from the CSGO Float API
          async with aiohttp.ClientSession() as session:
              async with session.get(csgoFloatRawData) as resp:
                  resp = await resp.text()
                  rawData = ast.literal_eval(resp)
                  weaponname = rawData['iteminfo']['full_item_name']
                  paintseed = str(rawData['iteminfo']['paintseed'])
                  paintindex = str(rawData['iteminfo']['paintindex'])
                  defindex = str(rawData['iteminfo']['defindex'])
                  rarityname = str(rawData['iteminfo']['rarity_name'])
                  floatvalue = str(rawData['iteminfo']['floatvalue'])
                  stickerList = rawData['iteminfo']['stickers']
                  numberOfStickers = len(stickerList)
                  color1 = await getColor(rarityname)
                  steamnameurl = 'https://steamcommunity.com/market/listings/730/'
                  weaponUrlRaw = weaponname.replace(')','%29').replace(' ','%20')
                  weaponurl = steamnameurl+weaponUrlRaw

                  if (len(stickerList)== 0):
                      nostickers = True
                  else:
                      nostickers = False
                      try:
                          steamStickerUrl = 'https://steamcommunity.com/market/listings/730/Sticker%20%7C%20'
                          stickerRaw1 = rawData['iteminfo']['stickers'][0]['name']
                          stickerUrl1 = steamStickerUrl+stickerRaw1.replace(')','%29').replace(' ','%20')
                          stickerRaw2 = rawData['iteminfo']['stickers'][1]['name']
                          stickerUrl2 = steamStickerUrl+stickerRaw2.replace(')','%29').replace(' ','%20')
                          stickerRaw3 = rawData['iteminfo']['stickers'][2]['name']
                          stickerUrl3 = steamStickerUrl+stickerRaw3.replace(')','%29').replace(' ','%20')
                          stickerRaw4 = rawData['iteminfo']['stickers'][3]['name']
                          stickerUrl4 = steamStickerUrl+stickerRaw4.replace(')','%29').replace(' ','%20')
                          stickerRaw5 = rawData['iteminfo']['stickers'][4]['name']
                          stickerUrl5 = steamStickerUrl+stickerRaw5.replace(')','%29').replace(' ','%20')
                      except:
                          pass
          async with aiohttp.ClientSession() as session:
              async with session.get(screenshotURL) as resp:        
                  
                  # Define the generic embed
                  desc = ctx.author.mention + ', here\'s your screenshot.'
                  embed = discord.Embed(title="CS:GO Skin Screenshot", description=desc, url ='https://cheddydev.com/', color=color1, timestamp = datetime.datetime.utcnow())
                  wea = 'Name: **['+weaponname+']('+weaponurl+')** \nFloat: **' +floatvalue +'**\nQuality: **'+ rarityname + '**\nPaint Seed: **'+ paintseed +'**\nPaint Index: **'+ paintindex+ '**\nDefindex: **'+defindex+'**'
                  linkz = '[Screenshot]('+screenshotURL+')'
                  error = 'Could not get the screenshot! CSGO.Gallery is probably down right now.'
                  embed.add_field(name="Weapon Information:", value=wea, inline=False)
                  embed.set_footer(text="Screenshot Taken:", icon_url="https://cdn.discordapp.com/avatars/217440011451105280/7752b9953c981fe9b072dd0949e956f4.png?size=128")
                  print(rawData['iteminfo'])
                  if ('killeatervalue' in rawData['iteminfo']):
                      stKills = str(rawData['iteminfo']['killeatervalue'])
                      wea = 'Name: **['+weaponname+']('+weaponurl+')** \nStatTrak™ Kills: **'+stKills+'** \nFloat: **' +floatvalue +'**\nQuality: **'+ rarityname + '**\nPaint Seed: **'+ paintseed +'**\nPaint Index: **'+ paintindex+ '**\nDefindex: **'+defindex+'**'
                      
                  # Print the embed if there aren't any stickers
                  if nostickers == True:
                      if (resp.status == 200):
                          embed.set_image(url=screenshotURL)
                          embed.add_field(name="Image Link:", value=linkz, inline=False)
                          await ctx.channel.send(embed=embed)
                      else:
                          embed.add_field(name="ERROR:", value=error, inline=False)
                          await ctx.channel.send(embed=embed)

                  # Print the embed with stickers
                  else:
                      if numberOfStickers == 1:
                          stickers = '**['+stickerRaw1+']('+stickerUrl1+')**'
                      elif numberOfStickers == 2:
                          stickers = '**['+stickerRaw1+']('+stickerUrl1+')**\n**['+stickerRaw2+']('+stickerUrl2+')**'
                      elif numberOfStickers == 3:
                          stickers = '**['+stickerRaw1+']('+stickerUrl1+')**\n**['+stickerRaw2+']('+stickerUrl2+')**\n**['+stickerRaw3+']('+stickerUrl3+')**'
                      elif numberOfStickers == 4:
                          stickers = '**['+stickerRaw1+']('+stickerUrl1+')**\n**['+stickerRaw2+']('+stickerUrl2+')**\n**['+stickerRaw3+']('+stickerUrl3+')**\n**['+stickerRaw4+']('+stickerUrl4+')**'
                      elif numberOfStickers == 5:
                          stickers = '**['+stickerRaw1+']('+stickerUrl1+')**\n**['+stickerRaw2+']('+stickerUrl2+')**\n**['+stickerRaw3+']('+stickerUrl3+')**\n**['+stickerRaw4+']('+stickerUrl4+')**\n**['+stickerRaw5+']('+stickerUrl5+')**'
                      embed.add_field(name="Stickers:", value=stickers, inline=False)
                      if(resp.status == 200):
                          embed.set_image(url=screenshotURL)
                          embed.add_field(name="Image Link:", value=linkz, inline=False)
                          await ctx.channel.send(embed=embed)
                      else:
                          embed.add_field(name="ERROR:", value=error, inline=False)
                          await ctx.channel.send(embed=embed)

      # Checks inspect link and channel, if it's good, then go to get the image
      if ctx.channel.id == screenshotchannel:
          if ctx.author == self.bot.user:
            pass
          else:
            if ctx.content.startswith("steam://rungame/730/76561202255233023/+csgo_econ_action_preview"):
                await ctx.delete()
                await ctx.channel.send('Getting your screenshot, '+ ctx.author.mention+ ', please wait.',delete_after=15.0)
                async with ctx.channel.typing():
                    await getScreenshot()
            else:
              await ctx.delete()
              await ctx.channel.send('That is not a valid inspect link, ' + ctx.author.mention +'!',delete_after=8.0)

def setup(bot):
    bot.add_cog(screenshotTwo(bot))
