#This is currently unused, as csgo.gallery has been under maintenance for quite some time.

import discord
import aiohttp
import asyncio
import requests
import datetime
from discord.ext import commands

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
      global url
      global threeD
      async def getdata():
          global floatvalue
          global rarityname
          global color1
          global weaponname
          global sticker0
          global sticker1
          global sticker2
          global sticker3
          global sticker4
          global nostickers
          global numberofstickers
          global stickerurl0
          global stickerurl1
          global stickerurl2
          global stickerurl3
          global stickerurl4
          global paintseed
          global defindex
          global paintindex
          global weaponurl
          color1 = 0X02FE0E
          resp = requests.get(floatraw)
          rawdata1 = resp.content.decode()
          stickerdata = rawdata1.split(',')
          rawdata2 = rawdata1.replace(',',' ')
          rawdata = rawdata2.split()
          #Getting the weapon and skin name.
          weaponskinindex1 = [i for i, elem in enumerate(rawdata) if 'full_item_name' in elem]
          weaponskinindex2 = ''.join([str(i) for i in weaponskinindex1])
          weaponskinindex = int(weaponskinindex2)
          weaponskin1 = rawdata[weaponskinindex:]
          weaponname1 = ' '.join(weaponskin1)
          weaponname2 = weaponname1.replace('\"full_item_name\":\"','')
          weaponname3 = weaponname2.replace('\"','')
          weaponname = weaponname3.replace('}','')
          steamnameurl = 'https://steamcommunity.com/market/listings/730/'
          weaponurlbasic1 = weaponname.replace(')','%29')
          weaponurlbasic = weaponurlbasic1.replace(' ','%20')
          weaponurl = steamnameurl+weaponurlbasic
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
          if rarityname == 'Industrial':
              color1 = 0X77A5FF
          if rarityname == 'Mil-Spec':
              color1 = 0X3C66DA
          if rarityname == 'Restricted':
              color1 = 0X893AE7
          if rarityname == 'Classified':
              color1 = 0XD437D2
          if rarityname == 'Covert':
              color1 = 0XE81E02
          if rarityname == 'Contraband':
              color1 = 0XB88132
          #Getting the stickers.
          stickerindex1 = [i for i, elem in enumerate(stickerdata) if '\"name\"' in elem]
          numberofstickers = len(stickerindex1)
          if numberofstickers == 0:
              nostickers = True
              pass
          else:
              nostickers = False
              try:
                  steamstickerurl = 'https://steamcommunity.com/market/listings/730/Sticker%20%7C%20'
                  stickerindex = int(stickerindex1[0])
                  stickers1 = stickerdata[stickerindex]
                  stickers2 = stickers1.replace('\"name\":\"','')
                  stickers3 = stickers2.replace(']','')
                  sticker0 = stickers3.replace('\"}','')
                  sticker00 = sticker0.replace(')','%29')
                  stickerreplace = sticker00.replace(' ','%20')
                  stickerurl0 = steamstickerurl+stickerreplace
                  stickerindex = int(stickerindex1[1])
                  stickers1 = stickerdata[stickerindex]
                  stickers2 = stickers1.replace('\"name\":\"','')
                  stickers3 = stickers2.replace(']','')
                  sticker1 = stickers3.replace('\"}','')
                  sticker11 = sticker1.replace(')','%29')
                  stickerreplace = sticker11.replace(' ','%20')
                  stickerurl1 = steamstickerurl+stickerreplace
                  stickerindex = int(stickerindex1[2])
                  stickers1 = stickerdata[stickerindex]
                  stickers2 = stickers1.replace('\"name\":\"','')
                  stickers3 = stickers2.replace(']','')
                  sticker2 = stickers3.replace('\"}','')
                  sticker22 = sticker2.replace(')','%29')
                  stickerreplace = sticker22.replace(' ','%20')
                  stickerurl2 = steamstickerurl+stickerreplace
                  stickerindex = int(stickerindex1[3])
                  stickers1 = stickerdata[stickerindex]
                  stickers2 = stickers1.replace('\"name\":\"','')
                  stickers3 = stickers2.replace(']','')
                  sticker3 = stickers3.replace('\"}','')
                  sticker33 = sticker3.replace(')','%29')
                  stickerreplace = sticker33.replace(' ','%20')
                  stickerurl3 = steamstickerurl+stickerreplace
                  stickerindex = int(stickerindex1[4])
                  stickers1 = stickerdata[stickerindex]
                  stickers2 = stickers1.replace('\"name\":\"','')
                  stickers3 = stickers2.replace(']','')
                  sticker4 = stickers3.replace('\"}','')
                  sticker44 = sticker4.replace(')','%29')
                  stickerreplace = sticker44.replace(' ','%20')
                  stickerurl4 = steamstickerurl+stickerreplace
              except:
                  pass
          #Getting the float value.
          floatindex1 = [i for i, elem in enumerate(rawdata) if 'floatvalue' in elem]
          floatindex2 = ''.join([str(i) for i in floatindex1])
          floatindex = int(floatindex2)
          floatvalue1 = rawdata[floatindex]
          floatvalue = floatvalue1.replace('\"floatvalue\":','')
          
      async def getimage(): #Gets the screenshot from csgo.gallery.
        global floatvalue
        async with aiohttp.ClientSession() as session:   
            async with session.get(url) as resp:
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
                  await asyncio.sleep(2)
              else:
                  if numberofstickers == 1:
                      stickers = '**['+sticker0+']('+stickerurl0+')**'
                  if numberofstickers == 2:
                      stickers = '**['+sticker0+']('+stickerurl0+')**\n**['+sticker1+']('+stickerurl1+')**'
                  if numberofstickers == 3:
                      stickers = '**['+sticker0+']('+stickerurl0+')**\n**['+sticker1+']('+stickerurl1+')**\n**['+sticker2+']('+stickerurl2+')**'
                  if numberofstickers == 4:
                      stickers = '**['+sticker0+']('+stickerurl0+')**\n**['+sticker1+']('+stickerurl1+')**\n**['+sticker2+']('+stickerurl2+')**\n**['+sticker3+']('+stickerurl3+')**'
                  if numberofstickers == 5:
                      stickers = '**['+sticker0+']('+stickerurl0+')**\n**['+sticker1+']('+stickerurl1+')**\n**['+sticker2+']('+stickerurl2+')**\n**['+sticker3+']('+stickerurl3+')**\n**['+sticker4+']('+stickerurl4+')**'
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
                      if numberofstickers == 1:
                          stickers = '**['+sticker0+']('+stickerurl0+')**'
                      if numberofstickers == 2:
                          stickers = '**['+sticker0+']('+stickerurl0+')**\n**['+sticker1+']('+stickerurl1+')**'
                      if numberofstickers == 3:
                          stickers = '**['+sticker0+']('+stickerurl0+')**\n**['+sticker1+']('+stickerurl1+')**\n**['+sticker2+']('+stickerurl2+')**'
                      if numberofstickers == 4:
                          stickers = '**['+sticker0+']('+stickerurl0+')**\n**['+sticker1+']('+stickerurl1+')**\n**['+sticker2+']('+stickerurl2+')**\n**['+sticker3+']('+stickerurl3+')**'
                      if numberofstickers == 5:
                          stickers = '**['+sticker0+']('+stickerurl0+')**\n**['+sticker1+']('+stickerurl1+')**\n**['+sticker2+']('+stickerurl2+')**\n**['+sticker3+']('+stickerurl3+')**\n**['+sticker4+']('+stickerurl4+')**'
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

      if ctx.channel.id == 494905423393062912: #Checks inspect link, if its good then go to get the image.
          if ctx.author == self.bot.user:
            pass
          else:
            if ctx.content.startswith("steam://rungame/730/76561202255233023/+csgo_econ_action_preview"):
              global inspect
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
                  await getimage()
            else:
              await ctx.delete()
              await ctx.channel.send('That is not a valid inspect link, ' + ctx.author.mention +'!',delete_after=8.0)

def setup(bot):
    bot.add_cog(screenshot(bot))
