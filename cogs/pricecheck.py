import discord  
import aiohttp
from discord.ext import commands
import re

key = '' #csgo backpack api key


class priceCheck(commands.Cog, name="Price check command"):
  def __init__(self, bot):
        self.bot = bot


  @commands.command(name='pc')
  async def pc(self, ctx): #Price check command.
    two='%20'
    blue = 0X3249DA
    red = 0XE81E02
    yellow = 0XDFDB00

    async def getprice(): 
      async with ctx.typing():
          global price
          global skinlink
          global icon
          global steamlink
          global bitskins
          global sold
          global lowest
          global highest
          async with aiohttp.ClientSession() as session:
              async with session.get('https://csgobackpack.net/api/GetItemPrice/?currency=USD&id='+skinlink+'&time=300&icon=1&key='+key) as resp:
                  resp = await resp.text()
          steamlinktest=skinlink.replace(')','%29')
          steamlink1='https://steamcommunity.com/market/listings/730/'+steamlinktest
          steamlink = steamlink1.replace(' ','%20')
          bitskins1='https://bitskins.com/?app_id=730&market_hash_name='+steamlinktest
          bitskins = bitskins1.replace(' ','%20')
          data1 = resp.replace(',',' ')
          rawdata = data1.split()
          lowest = rawdata[5].replace('\"','').replace('lowest_price:','')
          highest = rawdata[6].replace('\"','').replace('highest_price:','')
          icon = rawdata[9].replace('\"','').replace('icon:','').replace('\\','')
          sold= rawdata[3].replace('\"','').replace('amount_sold:','')
          price = rawdata[1] .replace('\"','').replace(':','').replace('average_price','')
          await displayPrice()
    
    async def displayPrice():
        #TODO: Replace link with steam page.
        global thumbnail
        global price
        global color
        desc1='The average price for \n' +'**'+gunname+'** is: **$'+price+'**\n\nAmount sold: **'+sold+'**\nLowest price sold for: **$'+lowest+'**\nHighest price sold for: **$'+highest+'**'
        #desc1='The average steam market price in the past 30 days for \n' +'**'+gunname+'** is: **$'+price+'**\n\nAmount sold on the steam market in the past 30 days: **'+sold+'**\nLowest price on the steam market in the past 30 days: **$'+lowest+'**\nHighest price on the steam market in the past 30 days: **$'+highest+'**'timestamp = datetime.datetime.utcnow()
        embed = discord.Embed(title="Price Check", description=desc1, url=icon,  color=color)
        links = "[Steam Market]("+steamlink+")\n[Bitskins]("+bitskins+")\n_ _"
        embed.add_field(name="Links", value=links, inline=False)
        embed.set_thumbnail(url=icon)
        embed.set_footer(text="All data is from the steam marketplace from the past 30 days", icon_url="https://cdn.discordapp.com/avatars/217440011451105280/7752b9953c981fe9b072dd0949e956f4.png?size=128")
        await ctx.send(embed=embed)

    remove = ctx.message.content
    remove1 = remove[0:4]
    pc1 = remove.replace(remove1, '')
    if pc1 == "":
        await ctx.send('!pc cannot be empty, '+ ctx.message.author.mention+'. Type !pc help to get started!')
    
    else:
        if "(" in pc1 or ")":
            pc = pc1.replace('(', '').replace(')', '')
        pc = (' '.join([w.title() if w.islower() else w for w in pc.split()])).split()
        pclength = len(pc)
        pc[pclength-1] = pc[pclength-1]+')'
        pc[pclength-2] = '('+pc[pclength-2]
        pc = " ".join(pc)
        if pc == "(Help)":
            desc = 'This command returns a skin\'s average steam market price, as well as the amount sold on the steam market, both for the past 30 days.'
            format1 = 'Make sure you have the correct formatting of the weapon name by checking here: <https://counterstrike.fandom.com/wiki/Category:Weapons> \n\nAll gun skins, knives, and gloves should be supported. Please <@217440011451105280> if you find a skin does not work.'
            pcs = '```!pc AK-47 Wasteland Rebel Battle Scarred\n!pc ST AK-47 The Empress Field Tested\n!pc Karambit Doppler Factory New\n!pc ST Bowie Knife Marble Fade Minimal Wear\n!pc Driver Gloves Lunar Weave Field Tested```'
            embed = discord.Embed(title="Price Check", description=desc, color=0X00CCCC)
            embed.add_field(name="Format", value=format1, inline=False)
            embed.add_field(name="Examples", value=pcs, inline=False)
            await ctx.send(embed=embed)
        else:
            try:
              pclist = re.sub('\\bst\\b', 'ST', pc, flags=re.I)
              pclist = re.sub('mp9\\b', 'MP9', pclist, flags=re.I)
              pclist = re.sub('usps\\b', 'USPS', pclist, flags=re.I)
              pclist = re.sub('usp-s\\b', 'USP-S', pclist, flags=re.I)
              pclist = re.sub('famas\\b', 'FAMAS', pclist, flags=re.I)
              pclist = re.sub('\\bsg\\b', 'SG', pclist, flags=re.I)
              pclist = re.sub('m4a4\\b', 'M4A4', pclist, flags=re.I)
              pclist = re.sub('m4a1s\\b', 'M4A1-S', pclist, flags=re.I)
              pclist = re.sub('m4a1-s\\b', 'M4A1-S', pclist, flags=re.I)
              pclist = re.sub('ak47\\b', 'AK-47', pclist, flags=re.I)
              pclist = re.sub('ak-47\\b', 'AK-47', pclist, flags=re.I)
              pclist = re.sub('five seven\\b', 'Five-SeveN', pclist, flags=re.I)
              pclist = re.sub('five-seven\\b', 'Five-SeveN', pclist, flags=re.I)
              pclist = re.sub('57\\b', 'Five-SeveN', pclist, flags=re.I)
              pclist = re.sub('5-7\\b', 'Five-SeveN', pclist, flags=re.I)
              pclist = re.sub('\\bar\\b', 'AR', pclist, flags=re.I)
              pclist = re.sub('ump45\\b', 'AR', pclist, flags=re.I)
              pclist = re.sub('ump-45\\b', 'AR', pclist, flags=re.I)
              pclist = pclist.split()
              st = 'StatTrak™'
              global skinlink 
              global color
              if pclist[0] == "Souvenir": #Souvenir skins.
                  color = yellow
                  if len(pclist) == 5:
                      gunname = pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]                        
                      if pclist[3].startswith("(Minimal") or pclist[3].startswith("(Factory"):
                          skinlink = pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+' '+pclist[4]
                          await getprice()   
                      else:
                        skinlink = pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+'-'+pclist[4]
                        await getprice()             
                  if len(pclist) == 6:                            
                      gunname = pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]                 
                      if pclist[4].startswith("(Minimal") or pclist[4].startswith("(Factory"):
                          skinlink = pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+' '+pclist[5]
                          await getprice()
                      else:
                        skinlink = pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+'-'+pclist[5]
                        await getprice()
                  if len(pclist) == 7:
                      gunname = pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]+' '+pclist[6]   
                      if pclist[5].startswith("(Minimal") or pclist[5].startswith("(Factory"):
                          skinlink = pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+two+pclist[5]+' '+pclist[5]
                          await getprice()
                      else:
                        skinlink = pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+two+pclist[5]+'-'+pclist[5]
                        await getprice()
              elif pclist[0] == "Desert" or pclist[1] == "Desert" or pclist[0] == "Dual" or pclist[1] == "Dual" or pclist[0] == "R8" or pclist[1] == "R8" or pclist[0] == "SG" or pclist[1] == "SG" or pclist[0] == "SSG" or pclist[1] == "SSG" or pclist[0] == "Galil" or pclist[1] == "Galil":
                  if pclist[0] == "ST": #ST 2 word gun anmes
                        color = red
                        if len(pclist) == 6:
                            gunname = st+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]                        
                            if pclist[4].startswith("(Minimal") or pclist[4].startswith("(Factory"):
                                skinlink = 'StatTrak™'+two+pclist[1]+two+pclist[2]+two+'|'+two+pclist[3]+two+pclist[4]+' '+pclist[5]
                                await getprice()   
                            else:
                              skinlink = 'StatTrak™'+two+pclist[1]+two+pclist[2]+two+'|'+two+pclist[3]+two+pclist[4]+'-'+pclist[5]
                              await getprice()             
                        if len(pclist) == 7:
                            gunname = st+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]+' '+pclist[6]                    
                            if pclist[5].startswith("(Minimal") or pclist[5].startswith("(Factory"):
                                skinlink = 'StatTrak™'+two+pclist[1]+two+pclist[2]+two+'|'+two+pclist[3]+two+pclist[4]+two+pclist[5]+' '+pclist[6]
                                await getprice()
                            else:
                              skinlink = 'StatTrak™'+two+pclist[1]+two+pclist[2]+two+'|'+two+pclist[3]+two+pclist[4]+two+pclist[5]+'-'+pclist[6]
                              await getprice()
                        if len(pclist) == 8:
                            gunname = st+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]+' '+pclist[6]+' '+pclist[7]
                            if pclist[6].startswith("(Minimal") or pclist[6].startswith("(Factory"):
                                skinlink = 'StatTrak™'+two+pclist[1]+two+pclist[2]+two+'|'+two+pclist[3]+two+pclist[4]+two+pclist[5]+two+pclist[6]+' '+pclist[6]
                                await getprice()
                            else:
                              skinlink = 'StatTrak™'+two+pclist[1]+two+pclist[2]+two+'|'+two+pclist[3]+two+pclist[4]+two+pclist[5]+two+pclist[6]+'-'+pclist[6]
                              await getprice()
                  else: #Regular 2 word gun names
                        color = blue
                        if len(pclist) == 5:
                            gunname = pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]                        
                            if pclist[3].startswith("(Minimal") or pclist[3].startswith("(Factory"):
                                skinlink = pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+' '+pclist[4]
                                await getprice()   
                            else:
                              skinlink = pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+'-'+pclist[4]
                              await getprice()             
                        if len(pclist) == 6:                            
                            gunname = pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]                 
                            if pclist[4].startswith("(Minimal") or pclist[4].startswith("(Factory"):
                                skinlink = pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+' '+pclist[5]
                                await getprice()
                            else:
                              skinlink = pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+'-'+pclist[5]
                              await getprice()
                        if len(pclist) == 7:
                            gunname = pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]+' '+pclist[6]   
                            if pclist[5].startswith("(Minimal") or pclist[5].startswith("(Factory"):
                                skinlink = pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+two+pclist[5]+' '+pclist[5]
                                await getprice()
                            else:
                              skinlink = pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+two+pclist[5]+'-'+pclist[5]
                              await getprice()
              else:
                  if pclist[1] == "Knife" or pclist[2] == "Knife" or pclist[1] == "Daggers" or pclist[2] == "Daggers" or pclist[0] == "M9" or pclist[1] == "M9" or pclist[1] == "Gloves" or pclist[1] == "Wraps":
                      color = yellow
                      if pclist[0] == "ST": #ST two word knives    
                              if len(pclist) == 6:
                                  gunname = st+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]
                                  if pclist[4].startswith("(Minimal") or pclist[4].startswith("(Factory"):
                                      skinlink = '★ StatTrak™'+two+pclist[1]+two+pclist[2]+two+'|'+two+pclist[3]+two+pclist[4]+' '+pclist[5]
                                      await getprice()
                                  else:
                                    skinlink = '★ StatTrak™'+two+pclist[1]+two+pclist[2]+two+'|'+two+pclist[3]+two+pclist[4]+'-'+pclist[5]
                                    await getprice()
                              if len(pclist) == 7:
                                  gunname = st+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]+' '+pclist[6]
                                  if pclist[5].startswith("(Minimal") or pclist[5].startswith("(Factory"):
                                      skinlink = '★ StatTrak™'+two+pclist[1]+two+pclist[2]+two+'|'+two+pclist[3]+two+pclist[4]+two+pclist[5]+' '+pclist[6]
                                      await getprice()
                                  else:
                                    skinlink = '★ StatTrak™'+two+pclist[1]+two+pclist[2]+two+'|'+two+pclist[3]+two+pclist[4]+two+pclist[5]+'-'+pclist[6]
                                    await getprice()
                              if len(pclist) == 8:
                                  gunname = st+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]+' '+pclist[6]+' '+pclist[7]
                                  if pclist[6].startswith("(Minimal") or pclist[6].startswith("(Factory"):
                                      skinlink = '★ StatTrak™'+two+pclist[1]+two+pclist[2]+two+'|'+two+pclist[3]+two+pclist[4]+two+pclist[5]+two+pclist[6]+' '+pclist[7]
                                      await getprice()
                                  else:
                                    skinlink = '★ StatTrak™'+two+pclist[1]+two+pclist[2]+two+'|'+two+pclist[3]+two+pclist[4]+two+pclist[5]+two+pclist[6]+'-'+pclist[7]
                                    await getprice()
                      else: #Two Word knives
                          color = yellow
                          if len(pclist) == 5:
                              gunname = '★ '+pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]                        
                              if pclist[3].startswith("(Minimal") or pclist[3].startswith("(Factory"):
                                  skinlink = '★ '+pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+' '+pclist[4]
                                  await getprice()                
                              else:
                                skinlink = '★ '+pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+'-'+pclist[4]
                                await getprice()                     
                          if len(pclist) == 6:
                              gunname = '★ '+pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]                         
                              if pclist[4].startswith("(Minimal") or pclist[4].startswith("(Factory"):
                                  skinlink = '★ '+pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+' '+pclist[5]
                                  await getprice()                         
                              else:
                                skinlink = '★ '+pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+'-'+pclist[5]
                                await getprice()
                          if len(pclist) == 7:
                              gunname = '★ '+pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]+' '+pclist[6]
                              if pclist[5].startswith("(Minimal") or pclist[5].startswith("(Factory"):
                                  skinlink = '★ '+pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+two+pclist[5]+' '+pclist[6]
                                  await getprice()
                              
                              else:
                                skinlink = '★ '+pclist[0]+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+two+pclist[5]+'-'+pclist[6]
                                await getprice()             
                  elif pclist[0] == "Bayonet" or pclist[1] == "Bayonet" or pclist[0] == "Karambit" or pclist[1] == "Karambit":
                      color = yellow
                      if pclist[0] == "M9" or pclist[1] == "M9":
                          pass               
                      else:
                          if pclist[0] == "ST": #ST one word knives                         
                              if len(pclist) == 5:
                                  gunname = st+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]                           
                                  if pclist[3].startswith("(Minimal") or pclist[3].startswith("(Factory"):
                                      skinlink = '★ StatTrak™'+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+' '+pclist[4]
                                      await getprice()                            
                                  else:
                                    skinlink = '★ StatTrak™'+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+'-'+pclist[4]
                                    await getprice()                         
                              if len(pclist) == 6:
                                  gunname = st+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]                              
                                  if pclist[4].startswith("(Minimal") or pclist[4].startswith("(Factory"):
                                      skinlink = '★ StatTrak™'+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+' '+pclist[5]
                                      await getprice()
                                  else:
                                    skinlink = '★ StatTrak™'+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+'-'+pclist[5]
                                    await getprice()
                              if len(pclist) == 7:
                                  gunname = st+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]+' '+pclist[6]
                                  if pclist[5].startswith("(Minimal") or pclist[5].startswith("(Factory"):
                                      skinlink = '★ StatTrak™'+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+two+pclist[5]+' '+pclist[6]
                                      await getprice()
                                  else:
                                    skinlink = '★ StatTrak™'+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+two+pclist[5]+'-'+pclist[6]
                                    await getprice()
                          else: #One word knives.
                              if len(pclist) == 4:
                                  gunname = '★ '+pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]                            
                                  if pclist[2].startswith("(Minimal") or pclist[2].startswith("(Factory"):
                                      skinlink = '★ '+pclist[0]+two+'|'+two+pclist[1]+two+pclist[2]+' '+pclist[3]
                                      await getprice()                           
                                  else:
                                    skinlink = '★ '+pclist[0]+two+'|'+two+pclist[1]+two+pclist[2]+'-'+pclist[3]
                                    await getprice()                       
                              if len(pclist) == 5:
                                  gunname = '★ '+pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]               
                                  if pclist[3].startswith("(Minimal") or pclist[3].startswith("(Factory"):
                                      skinlink = '★ '+pclist[0]+two+'|'+two+pclist[1]+two+pclist[2]+two+pclist[3]+' '+pclist[4]
                                      await getprice()                             
                                  else:
                                    skinlink = '★ '+pclist[0]+two+'|'+two+pclist[1]+two+pclist[2]+two+pclist[3]+'-'+pclist[4]
                                    await getprice()
                              if len(pclist) == 6:
                                  gunname = '★ '+pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5] 
                                  if pclist[4].startswith("(Minimal") or pclist[4].startswith("(Factory"):
                                      skinlink = '★ '+pclist[0]+two+'|'+two+pclist[1]+two+pclist[2]+two+pclist[3]+two+pclist[4]+' '+pclist[5]
                                      await getprice()                           
                                  else:
                                    skinlink = '★ '+pclist[0]+two+'|'+two+pclist[1]+two+pclist[2]+two+pclist[3]+two+pclist[4]+'-'+pclist[5]
                                    await getprice()
                  else:
                    if pclist[0] == "ST": #ST Guns
                        color = red
                        if len(pclist) == 5:
                            gunname = st+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]                       
                            if pclist[3].startswith("(Minimal") or pclist[3].startswith("(Factory"):
                                skinlink = 'StatTrak™'+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+' '+pclist[4]
                                await getprice()   
                            else:
                              skinlink = 'StatTrak™'+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+'-'+pclist[4]
                              await getprice()             
                        if len(pclist) == 6:
                            gunname = st+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]                  
                            if pclist[4].startswith("(Minimal") or pclist[4].startswith("(Factory"):
                                skinlink = 'StatTrak™'+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+' '+pclist[5]
                                await getprice()
                            else:
                              skinlink = 'StatTrak™'+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+'-'+pclist[5]
                              await getprice()
                        if len(pclist) == 7:
                            gunname = st+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]+' '+pclist[6]
                            if pclist[5].startswith("(Minimal") or pclist[5].startswith("(Factory"):
                                skinlink = 'StatTrak™'+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+two+pclist[5]+' '+pclist[6]
                                await getprice()
                            else:
                              skinlink = 'StatTrak™'+two+pclist[1]+two+'|'+two+pclist[2]+two+pclist[3]+two+pclist[4]+two+pclist[5]+'-'+pclist[6]
                              await getprice()
                    else: #Regular Guns
                        color = blue               
                        if len(pclist) == 4:
                            gunname = pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]
                            if pclist[2].startswith("(Minimal") or pclist[2].startswith("(Factory"):
                                skinlink = pclist[0]+two+'|'+two+pclist[1]+two+pclist[2]+' '+pclist[3]
                                await getprice()                 
                            else:
                              skinlink = skinlink = pclist[0]+two+'|'+two+pclist[1]+two+pclist[2]+'-'+pclist[3]
                              await getprice()  
                        if len(pclist) == 5:
                            gunname = pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]                  
                            if pclist[3].startswith("(Minimal") or pclist[3].startswith("(Factory"):
                                skinlink = pclist[0]+two+'|'+two+pclist[1]+two+pclist[2]+two+pclist[3]+' '+pclist[4]
                                await getprice()                      
                            else:
                              skinlink = pclist[0]+two+'|'+two+pclist[1]+two+pclist[2]+two+pclist[3]+'-'+pclist[4]
                              await getprice()
                        if len(pclist) == 6:
                            gunname = pclist[0]+' '+pclist[1]+' '+pclist[2]+' '+pclist[3]+' '+pclist[4]+' '+pclist[5]
                            if pclist[4].startswith("(Minimal") or pclist[4].startswith("(Factory"):
                                skinlink = pclist[0]+two+'|'+two+pclist[1]+two+pclist[2]+two+pclist[3]+two+pclist[4]+' '+pclist[5]
                                await getprice()                      
                            else:
                              skinlink = pclist[0]+two+'|'+two+pclist[1]+two+pclist[2]+two+pclist[3]+two+pclist[4]+'-'+pclist[5]
                              await getprice()
            except IndexError:
                desc= ctx.message.author.mention+', I wasn\'t able to price check the "**'+gunname+'**"\n\nBefore trying again, make sure all words in your commmand are capitilized and spelled correctly. If you are still lost, please type ***!pc help***' 
                embed = discord.Embed(title="Whoops...", description=desc, color=0X000000)
                embed.set_footer(text="If all else fails, please ping @cheddy.")
                await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(priceCheck(bot))
