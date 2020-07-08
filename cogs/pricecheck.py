import discord
import datetime
import requests
from discord.ext import commands

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
          resp = requests.get('https://csgobackpack.net/api/GetItemPrice/?currency=USD&id='+skinlink+'&time=300&icon=1&key='+key)
          steamlinktest=skinlink.replace(')','%29')
          steamlink1='https://steamcommunity.com/market/listings/730/'+steamlinktest
          steamlink = steamlink1.replace(' ','%20')
          bitskins1='https://bitskins.com/?app_id=730&market_hash_name='+steamlinktest
          bitskins = bitskins1.replace(' ','%20')
          data1 = resp.text.replace(',',' ')
          rawdata = data1.split()
          averagepriceraw=rawdata[1]
          iconraw = rawdata[9]
          icon1 = iconraw.replace('\"','')
          icon2 = icon1.replace('icon','')
          icon3 = icon2.replace('\\','')
          icon = icon3[1:]
          soldraw= rawdata[3]
          sold1= soldraw.replace('\"','')
          sold2= sold1.replace('amount_sold','')
          sold3= sold2.replace('\\','')
          sold = sold3.replace(':','')
          pricestring = "average_price"
          price1 = averagepriceraw.replace('\"','')
          price2 = price1.replace(':','')
          price = price2.replace(pricestring,'')
          await displayPrice1()
    
    async def displayPrice1():
        #TODO: Replace link with steam page.
        global thumbnail
        global price
        global color
        desc1='The average steam market price in the past 30 days for \n' +'**'+gunname+'** is: **$'+price+'**\n\nAmount sold on the steam market in the past 30 days: **'+sold+'**'
        embed = discord.Embed(title="Price Check", description=desc1, url=icon,  color=color, timestamp = datetime.datetime.utcnow())
        links = "[Steam Market]("+steamlink+")\n[Bitskins]("+bitskins+")\n_ _"
        embed.add_field(name="Links", value=links, inline=False)
        embed.set_thumbnail(url=icon)
        embed.set_footer(text="Price Checked:", icon_url="https://cdn.discordapp.com/avatars/217440011451105280/7752b9953c981fe9b072dd0949e956f4.png?size=128")
        await ctx.send(embed=embed)
    remove = ctx.message.content
    remove1 = remove[0:4]
    pc1 = remove.replace(remove1, '')
    if "(" in pc1 or ")":
        pc2 = pc1.replace('(', '')
        pc3 = pc2.replace(')', '')
    pc4 = ' '.join([w.title() if w.islower() else w for w in pc3.split()])  
    pc5 = pc4.split()
    pclength = len(pc5)
    pc5[pclength-1] = pc5[pclength-1]+')'
    pc5[pclength-2] = '('+pc5[pclength-2]
    pc = " ".join(pc5)
    if pc == "()":
        await ctx.send('!pc cannot be empty, '+ ctx.message.author.mention+'. Type !pc help to get started!')
    elif pc == "(Help)":
        desc = 'This command returns a skin\'s average steam market price, as well as the amount sold on the steam market, both for the past 30 days.'
        format1 = 'Make sure you have the correct formatting of the weapon name by checking here: <https://counterstrike.fandom.com/wiki/Category:Weapons> \n\nAll gun skins, knives, and gloves should be supported. Please <@217440011451105280> if you find a skin does not work.'
        pcs = '```!pc AK-47 Wasteland Rebel Battle Scarred\n!pc ST AK-47 The Empress Field Tested\n!pc Karambit Doppler Factory New\n!pc ST Bowie Knife Marble Fade Minimal Wear\n!pc Driver Gloves Lunar Weave Field Tested```'
        embed = discord.Embed(title="Price Check", description=desc, color=0X00CCCC)
        embed.add_field(name="Format", value=format1, inline=False)
        embed.add_field(name="Examples", value=pcs, inline=False)
        await ctx.send(embed=embed)
    else:
        try:
          pclist = pc.split()
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
          elif pclist[0] == "Desert" or pclist[1] == "Desert" or pclist[0] == "Dual" or pclist[1] == "Dual" or pclist[0] == "R8" or pclist[1] == "R8" or pclist[0] == "SG" or pclist[1] == "SG" or pclist[0] == "SSG" or pclist[1] == "SSG":
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
            embed.set_footer(text="If all else fails, please ping @cheddy#7744.")
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(priceCheck(bot))
