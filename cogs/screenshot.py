import discord
import aiohttp
import asyncio
import requests
import datetime
from discord.ext import commands
screenshotchannel = 569901952545325056
class screenshot(commands.Cog, name="Screenshot"):
  def __init__(self, bot):
      self.bot = bot
    
  @commands.Cog.listener()
  async def on_message(self, ctx):
    guild = ctx.guild
    if guild == None:
        return
    else:
      global data
      global threeD
      async def getdata():
          global floatvalue
          global rarityname
          global color1
          global weaponname
          global stickerRaw1
          global stickerRaw2
          global stickerRaw3
          global stickerRaw4
          global stickerRaw5
          global nostickers
          global numberOfStickers
          global stickerUrl1
          global stickerUrl2
          global stickerUrl3
          global stickerUrl4
          global stickerUrl5
          global paintseed
          global defindex
          global paintindex
          global weaponurl
          color1 = 0X02FE0E
          resp = requests.get(floatraw)
          rawdata1 = resp.content.decode()
          stickerData = rawdata1.split(',')
          rawdata2 = rawdata1.replace(',',' ')
          rawdata = rawdata2.split()
          #Getting the weapon and skin name.
          weaponskinindex1 = [i for i, elem in enumerate(rawdata) if 'full_item_name' in elem]
          weaponskinindex2 = ''.join([str(i) for i in weaponskinindex1])
          weaponskinindex = int(weaponskinindex2)
          weaponskin1 = rawdata[weaponskinindex:]
          weaponname1 = ' '.join(weaponskin1)
          weaponname = weaponname1.replace('\"full_item_name\":\"','').replace('\"','').replace('}','')
          steamnameurl = 'https://steamcommunity.com/market/listings/730/'
          weaponUrlRaw = weaponname.replace(')','%29').replace(' ','%20')
          weaponurl = steamnameurl+weaponUrlRaw
          #Getting the paint seed, paint index, and defindex.
          paintseedindex1 = [i for i, elem in enumerate(rawdata) if 'paintseed' in elem]
          paintseedindex2 = ''.join([str(i) for i in paintseedindex1])
          paintseedindex = int(paintseedindex2)
          paintseed1 = rawdata[paintseedindex]
          paintseed2 = paintseed1.replace('\"paintseed\":','')
          paintseed = paintseed2.replace('\'','')
          paintindexindex1 = [i for i, elem in enumerate(rawdata) if 'paintindex' in elem]
          paintindexindex2 = ''.join([str(i) for i in paintindexindex1])
          paintindexindex = int(paintindexindex2)
          paintindex1 = rawdata[paintindexindex]
          paintindex2 = paintindex1.replace('\"paintindex\":','')
          paintindex = paintindex2.replace('\'','')
          defindexindex1 = [i for i, elem in enumerate(rawdata) if 'defindex' in elem]
          defindexindex2 = ''.join([str(i) for i in defindexindex1])
          defindexindex = int(defindexindex2)
          defindex1 = rawdata[defindexindex]
          defindex2 = defindex1.replace('\"defindex\":','')
          defindex = defindex2.replace('\'','')
          #Getting the weapon rarity name and color.
          rarityindex1 = [i for i, elem in enumerate(rawdata) if 'rarity_name' in elem]
          rarityindex2 = ''.join([str(i) for i in rarityindex1])
          rarityindex = int(rarityindex2)
          rarityname1 = rawdata[rarityindex]
          rarityname2 = rarityname1.replace('\"rarity_name\":','')
          rarityname = rarityname2.replace('\"','')
          if rarityname == 'Consumer':
              color1 = 0XC2C2C2
          elif rarityname == 'Industrial':
              color1 = 0X77A5FF
          elif rarityname == 'Mil-Spec':
              color1 = 0X3C66DA
          elif rarityname == 'Restricted':
              color1 = 0X893AE7
          elif rarityname == 'Classified':
              color1 = 0XD437D2
          elif rarityname == 'Covert':
              color1 = 0XE81E02
          else:
              color1 = 0XB88132
          #Getting the stickers.
          stickerIndex = [i for i, elem in enumerate(stickerData) if '\"name\"' in elem]
          numberOfStickers = len(stickerIndex)
          if numberOfStickers == 0:
              nostickers = True
              pass
          else:
              nostickers = False
              try:
                  steamStickerUrl = 'https://steamcommunity.com/market/listings/730/Sticker%20%7C%20'
                  stickerIndex1 = int(stickerIndex[0])
                  stickerRaw1 = stickerData[stickerIndex1].replace('\"name\":\"','').replace(']','').replace('\"}','')
                  stickerUrl1 = steamStickerUrl+stickerRaw1.replace(')','%29').replace(' ','%20')
                  stickerIndex2 = int(stickerIndex[1])
                  stickerRaw2 = stickerData[stickerIndex2].replace('\"name\":\"','').replace(']','').replace('\"}','')
                  stickerUrl2 = steamStickerUrl+stickerRaw2.replace(')','%29').replace(' ','%20')
                  stickerIndex3 = int(stickerIndex[2])
                  stickerRaw3 = stickerData[stickerIndex3].replace('\"name\":\"','').replace(']','').replace('\"}','')
                  stickerUrl3 = steamStickerUrl+stickerRaw3.replace(')','%29').replace(' ','%20')
                  stickerIndex4 = int(stickerIndex[3])
                  stickerRaw4 = stickerData[stickerIndex4].replace('\"name\":\"','').replace(']','').replace('\"}','')
                  stickerUrl4 = steamStickerUrl+stickerRaw4.replace(')','%29').replace(' ','%20')
                  stickerIndex5 = int(stickerIndex[4])
                  stickerRaw5 = stickerData[stickerIndex5].replace('\"name\":\"','').replace(']','').replace('\"}','')
                  stickerUrl5 = steamStickerUrl+stickerRaw5.replace(')','%29').replace(' ','%20')
              except:
                  pass
          #Getting the float value.
          floatindex1 = [i for i, elem in enumerate(rawdata) if 'floatvalue' in elem]
          floatindex2 = ''.join([str(i) for i in floatindex1])
          floatindex = int(floatindex2)
          floatvalue1 = rawdata[floatindex]
          floatvalue = floatvalue1.replace('\"floatvalue\":','')
          
      async def getimage(url): #Gets the screenshot from csgo.gallery.
        global floatvalue
        async with aiohttp.ClientSession() as session:  
            async with session.post(url) as resp:
              #TODO: Add more data values, add weapon thumbnail to the embed.
              if nostickers == True:
                  desc = ctx.author.mention + ', here\'s your screenshot.'
                  embed = discord.Embed(title="CS:GO Skin Screenshot", description=desc, url='https://cheddydev.com/', color=color1, timestamp = datetime.datetime.utcnow())
                  linkz= '[Screenshot]('+url+')'
                  embed.set_image(url=url)
                  wea = 'Name: **['+weaponname+']('+weaponurl+')** \nFloat: **' +floatvalue +'**\nQuality: **'+ rarityname + '**\nPaint Seed: **'+ paintseed +'**\nPaint Index: **'+ paintindex+ '**\nDefindex: **'+defindex+'**'
                  embed.add_field(name="Weapon Information:", value=wea, inline=False)
                  embed.add_field(name="Image Link:", value=linkz, inline=False)
                  embed.set_footer(text="Screenshot Taken:", icon_url="https://cdn.discordapp.com/avatars/217440011451105280/7752b9953c981fe9b072dd0949e956f4.png?size=128")
                  msg = await ctx.channel.send(embed=embed)
                  msg
              else:
                  if numberOfStickers == 1:
                      stickers = '**['+stickerRaw1+']('+stickerUrl1+')**'
                  if numberOfStickers == 2:
                      stickers = '**['+stickerRaw1+']('+stickerUrl1+')**\n**['+stickerRaw2+']('+stickerUrl2+')**'
                  if numberOfStickers == 3:
                      stickers = '**['+stickerRaw1+']('+stickerUrl1+')**\n**['+stickerRaw2+']('+stickerUrl2+')**\n**['+stickerRaw3+']('+stickerUrl3+')**'
                  if numberOfStickers == 4:
                      stickers = '**['+stickerRaw1+']('+stickerUrl1+')**\n**['+stickerRaw2+']('+stickerUrl2+')**\n**['+stickerRaw3+']('+stickerUrl3+')**\n**['+stickerRaw4+']('+stickerUrl4+')**'
                  if numberOfStickers == 5:
                      stickers = '**['+stickerRaw1+']('+stickerUrl1+')**\n**['+stickerRaw2+']('+stickerUrl2+')**\n**['+stickerRaw3+']('+stickerUrl3+')**\n**['+stickerRaw4+']('+stickerUrl4+')**\n**['+stickerRaw5+']('+stickerUrl5+')**'
                  desc = ctx.author.mention + ', here\'s your screenshot.'
                  embed = discord.Embed(title="CS:GO Skin Screenshot", description=desc, url='https://cheddydev.com/', color=color1, timestamp = datetime.datetime.utcnow())
                  linkz= '[Screenshot]('+url+')'
                  embed.set_image(url=url)
                  wea = 'Name: **['+weaponname+']('+weaponurl+')** \nFloat: **' +floatvalue +'**\nQuality: **'+ rarityname + '**\nPaint Seed: **'+ paintseed +'**\nPaint Index: **'+ paintindex+ '**\nDefindex: **'+defindex+'**'
                  embed.add_field(name="Weapon Information:", value=wea, inline=False)
                  embed.add_field(name="Stickers:", value=stickers, inline=False)
                  embed.add_field(name="Image Link:", value=linkz, inline=False)
                  embed.set_footer(text="Screenshot Taken:", icon_url="https://cdn.discordapp.com/avatars/217440011451105280/7752b9953c981fe9b072dd0949e956f4.png?size=128")
                  msg = await ctx.channel.send(embed=embed)
                  msg
                  await asyncio.sleep(2)
              if resp.status != 200:
                  if nostickers == True:
                      desc = ctx.author.mention + ', here\'s your screenshot.'
                      newembed = discord.Embed(title="CS:GO Skin Screenshot", description=desc, url='https://cheddydev.com/', color=color1, timestamp = datetime.datetime.utcnow())
                      linkz= '[Screenshot]('+url+')'
                      newembed.set_image(url=url)
                      wea = 'Name: **['+weaponname+']('+weaponurl+')** \nFloat: **' +floatvalue +'**\nQuality: **'+ rarityname + '**\nPaint Seed: **'+ paintseed +'**\nPaint Index: **'+ paintindex+ '**\nDefindex: **'+defindex+'**'
                      newembed.add_field(name="Weapon Information:", value=wea, inline=False)
                      newembed.add_field(name="Image Link:", value=linkz, inline=False)
                      newembed.set_footer(text="Screenshot Taken:", icon_url="https://cdn.discordapp.com/avatars/217440011451105280/7752b9953c981fe9b072dd0949e956f4.png?size=128")
                      await msg.edit(embed=newembed)
                  else:
                      if numberOfStickers == 1:
                          stickers = '**['+stickerRaw1+']('+stickerUrl1+')**'
                      if numberOfStickers == 2:
                          stickers = '**['+stickerRaw1+']('+stickerUrl1+')**\n**['+stickerRaw2+']('+stickerUrl2+')**'
                      if numberOfStickers == 3:
                          stickers = '**['+stickerRaw1+']('+stickerUrl1+')**\n**['+stickerRaw2+']('+stickerUrl2+')**\n**['+stickerRaw3+']('+stickerUrl3+')**'
                      if numberOfStickers == 4:
                          stickers = '**['+stickerRaw1+']('+stickerUrl1+')**\n**['+stickerRaw2+']('+stickerUrl2+')**\n**['+stickerRaw3+']('+stickerUrl3+')**\n**['+stickerRaw4+']('+stickerUrl4+')**'
                      if numberOfStickers == 5:
                          stickers = '**['+stickerRaw1+']('+stickerUrl1+')**\n**['+stickerRaw2+']('+stickerUrl2+')**\n**['+stickerRaw3+']('+stickerUrl3+')**\n**['+stickerRaw4+']('+stickerUrl4+')**\n**['+stickerRaw5+']('+stickerUrl5+')**'
                      desc = ctx.author.mention + ', here\'s your screenshot.'
                      newembed = discord.Embed(title="CS:GO Skin Screenshot", description=desc, url='https://cheddydev.com/', color=color1, timestamp = datetime.datetime.utcnow())
                      linkz= '[Screenshot]('+url+')'
                      newembed.set_image(url=url)
                      wea = 'Name: **['+weaponname+']('+weaponurl+')** \nFloat: **' +floatvalue +'**\nQuality: **'+ rarityname + '**\nPaint Seed: **'+ paintseed +'**\nPaint Index: **'+ paintindex+ '**\nDefindex: **'+defindex+'**'
                      newembed.add_field(name="Weapon Information:", value=wea, inline=False)
                      embed.add_field(name="Stickers:", value=stickers, inline=False)
                      newembed.add_field(name="Image Link:", value=linkz, inline=False)
                      newembed.set_footer(text="Screenshot Taken:", icon_url="https://cdn.discordapp.com/avatars/217440011451105280/7752b9953c981fe9b072dd0949e956f4.png?size=128")
                      await msg.edit(embed=newembed)


      if ctx.channel.id == screenshotchannel: #Checks inspect link, if its good then go to get the image.
          if ctx.author == self.bot.user:
            pass
          else:
            if ctx.content.startswith("steam://rungame/730/76561202255233023/+csgo_econ_action_preview"):
              global inspect
              global url
              floatwebsite = "https://api.csgofloat.com/?url="
              screenwebsite = "https://csgo.gallery/" 
              inspect = ctx.content
              url = screenwebsite+inspect
              floatraw = floatwebsite+inspect
              threeD = screenwebsite+'CSGO-3D-viewer'+inspect
              await ctx.delete()
              await ctx.channel.send('Getting your screenshot, '+ ctx.author.mention+ ', please wait.',delete_after=15.0)
              async with ctx.channel.typing():
                  await getdata()
                  await getimage(url)
            else:
              await ctx.delete()
              await ctx.channel.send('That is not a valid inspect link, ' + ctx.author.mention +'!',delete_after=8.0)

def setup(bot):
    bot.add_cog(screenshot(bot))
