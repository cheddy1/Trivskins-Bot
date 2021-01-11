import discord
import io
import aiohttp
import asyncio
from discord.ext import commands

serverid = 
modmail =  #modmail category id
modid= '' #mod role id
helperid= '' #helper role id
modmaillogging =  #modmail logging id


class Modmail(commands.Cog, name="Modmail Function"):
  def __init__(self, bot):
        self.bot = bot

  
  @commands.command(name='dm')
  async def sendDM(self, ctx):
      guild = ctx.message.guild
      await ctx.message.add_reaction('\U00002705')
      if guild == None:
          guild = self.bot.get_guild(serverid)
      category = guild.get_channel(modmail) 
      modmailloggingchannel =  guild.get_channel(modmaillogging)
      channel = await ctx.author.create_dm()
      author = str(ctx.author)
      global closereason

      def check(reaction, user):
          return user.id != self.bot.user.id
  
      def checkUser(reaction, user):
          return user.id != self.bot.user.id and user.id == ctx.author.id

      async def ban():
          await channel.send("Thanks for the report, "+ctx.author.mention+', the user you reported was banned, and the ticket has been closed. If you would like open a new one, just send me !dm')
          desc = "**"+reason+"**"
          reportee = '<@'+discID+'>\n'+discID
          reporter = ctx.author.mention+'\n'+str(ctx.author.id)
          moderator = '<@'+str(user.id)+'>'
          try: 
              await guild.ban(discord.Object(id=int(discID)),reason=reason, delete_message_days=7)
          except:
              desc=  "**"+reason+"**"+"\n**!ERROR!** User could not be banned."
          embed = discord.Embed(title="Report Ticket Closed", color=0Xf70000)
          embed.add_field(name="Reason Reported", value=desc, inline=False)
          embed.add_field(name="User Banned", value=reportee, inline=True)
          embed.add_field(name="Reporter", value=reporter, inline=True)
          embed.add_field(name="Moderator", value=moderator, inline=True)
          await modmailloggingchannel.send(embed=embed)
          await reportchannel.delete()

      async def closeReportTicket():
          end = user.mention+', please type the reason why you are closing the ticket. For example, \"No action is needed\" or \"Issue resolved\" and I\'ll close the ticket.'
          embed = discord.Embed(title="Closing Ticket", description=end, color=0Xed9632)
          await reportchannel.send(embed=embed)
          closereason = await self.bot.wait_for('message',check=lambda message: message.channel == reportchannel and message.author.id != self.bot.user.id)
          reasonreported = "**"+reason+"**"
          reasonclosed = "**"+closereason.content+"**"
          reportee = '<@'+discID+'>\n'+discID
          reporter = ctx.author.mention+'\n'+str(ctx.author.id)
          moderator = '<@'+str(user.id)+'>'
          embed = discord.Embed(title="Report Ticket Closed", color=0Xf70000)
          embed.add_field(name="Reason Reported", value=reasonreported, inline=False)
          embed.add_field(name="Reason Closed", value=reasonclosed, inline=False)
          embed.add_field(name="User Reported", value=reportee, inline=True)
          embed.add_field(name="Reporter", value=reporter, inline=True)
          embed.add_field(name="Moderator", value=moderator, inline=True)
          await modmailloggingchannel.send(embed=embed)
          await reportchannel.delete()

      async def closeSupportTicket():
          end = user.mention+', please type the reason why you are closing the ticket. For example, \"No action is needed\" or \"Issue resolved\" and I\'ll close the ticket.'
          embed = discord.Embed(title="Closing Ticket", description=end, color=0Xed9632)
          await supportchannel.send(embed=embed)
          closereason = await self.bot.wait_for('message',check=lambda message: message.channel == supportchannel and message.author.id != self.bot.user.id)
          closereasoncontent = closereason.content
          reporter = ctx.author.mention+'\n'+str(ctx.author.id)
          moderator = '<@'+str(user.id)+'>'
          embed = discord.Embed(title="Support/Feedback Ticket Closed",color=0Xe257fa)
          content = specialmessage.content
          embed.add_field(name="Reason Closed", value=closereasoncontent, inline=False)
          embed.add_field(name="User's Message", value=content, inline=False)
          embed.add_field(name="User", value=reporter, inline=True)
          embed.add_field(name="Moderator", value=moderator, inline=True)
          await modmailloggingchannel.send(embed=embed)
          await supportchannel.delete()
          
      desc = "Hey, what can I help you with?\n\n:one:: Report Another User\n:two:: Discord Support/Feedback\n:three:: Other"
      embed = discord.Embed(title="Open a Ticket", description=desc, color=0X57faea)
      embed.set_footer(text="This will timeout after 30 seconds of no response")
      opennewmodmail = await channel.send(embed=embed)
      await opennewmodmail.add_reaction('1\N{variation selector-16}\N{combining enclosing keycap}')
      await opennewmodmail.add_reaction('2\N{variation selector-16}\N{combining enclosing keycap}')
      await opennewmodmail.add_reaction('3\N{variation selector-16}\N{combining enclosing keycap}')
      try:
          userchoice, user = await self.bot.wait_for('reaction_add',check=checkUser,timeout=30)
      except asyncio.TimeoutError:
          await channel.send("Timed out! Please start over with !dm")
          return
          
      await opennewmodmail.remove_reaction('1\N{variation selector-16}\N{combining enclosing keycap}',self.bot.user)
      await opennewmodmail.remove_reaction('2\N{variation selector-16}\N{combining enclosing keycap}',self.bot.user)
      await opennewmodmail.remove_reaction('3\N{variation selector-16}\N{combining enclosing keycap}',self.bot.user)
      if str(userchoice.emoji) == '1\N{variation selector-16}\N{combining enclosing keycap}':
          desc = "What reason are you reporting for?\n\n:one:: Scamming\n:two:: Advertising\n:three:: Other"
          embed = discord.Embed(title="Report Reason", description=desc, color=0X57faea)
          embed.set_footer(text="This will timeout after 30 seconds of no response")
          reportreason = await channel.send(embed=embed)
          await reportreason.add_reaction('1\N{variation selector-16}\N{combining enclosing keycap}')
          await reportreason.add_reaction('2\N{variation selector-16}\N{combining enclosing keycap}')
          await reportreason.add_reaction('3\N{variation selector-16}\N{combining enclosing keycap}')
          try:
              userchoice2, user = await self.bot.wait_for('reaction_add',check=checkUser,timeout=30)
          except asyncio.TimeoutError:
              await channel.send("Timed out! Please start over with !dm")
              return
          if str(userchoice2.emoji) == '1\N{variation selector-16}\N{combining enclosing keycap}':
              reason = 'Scamming'
          if str(userchoice2.emoji) == '2\N{variation selector-16}\N{combining enclosing keycap}':
              reason = 'Advertising'
          if str(userchoice2.emoji) == '3\N{variation selector-16}\N{combining enclosing keycap}':
              reason = 'Other'
          await channel.send("Okay, let's report a user for "+reason+". Please send me either their discord name and # or their 18 digit discord dev ID.\n\nFormatting examples: \n`coolguy#1234`\n`12345678912345678` ")
          await reportreason.remove_reaction('1\N{variation selector-16}\N{combining enclosing keycap}',self.bot.user)
          await reportreason.remove_reaction('2\N{variation selector-16}\N{combining enclosing keycap}',self.bot.user)
          await reportreason.remove_reaction('3\N{variation selector-16}\N{combining enclosing keycap}',self.bot.user)
          try:
              discID1 = await self.bot.wait_for('message',check=lambda message: message.author == ctx.author and message.guild == None,timeout=120)
              if (any(c.isalpha() for c in discID1.content)):
                  try:
                      discID2 = await commands.UserConverter().convert(ctx,discID1.content)
                      discID = str(discID2.id)
                  except:
                      await channel.send("That's an invalid user! Send me their discord dev ID. This is usually a 18 digit long number.\nIf you do not know how to find it, please visit here: <https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID->\nIf you need help, please DM cheddy#7744")
                      try:
                          discID1 = await self.bot.wait_for('message',check=lambda message: message.author == ctx.author and message.guild == None,timeout=120)
                          discID = discID1.content
                      except asyncio.TimeoutError:
                          await channel.send("Timed out! Please start over with !dm")
                          return
              else:
                discID = discID1.content
          except asyncio.TimeoutError:
              await channel.send("Timed out! Please start over with !dm")
              return
          reportchannel = await guild.create_text_channel("Report - "+author, category=category)
          reportchannel
          desc = "Reason: "+reason
          reportee = 'Name: <@'+discID+'>\n'+discID
          reporter = 'Name: '+ctx.author.mention+'\n'+str(ctx.author.id)
          embed = discord.Embed(title="Report", description=desc, color=0Xfc2d2d)
          embed.add_field(name="User Being Reported", value=reportee, inline=True)
          embed.add_field(name="User Reporting", value=reporter, inline=True)
          await reportchannel.send(embed=embed)
          await channel.send("Now, please send all available proof to me, and I'll relay it to the moderators. Please type 'done' without the quotes once you are done sending the proof.")
          done = False
          while done == False:
              try:
                  proof = await self.bot.wait_for('message',check=lambda message: message.author == ctx.author and message.guild == None,timeout=180)
              except asyncio.TimeoutError:
                  await channel.send("Timed out! Please start over with !dm")
                  return
              if proof.content == 'done' or proof.content == 'Done':
                  done = True
                  await channel.send("Report ended. A moderator will process the report ASAP. If you need to add more evidence, please open another ticket by typing !dm")
                  end = ctx.author.mention+' has indicated the end of the report.'
                  reporter = ':white_check_mark:: to ban the reported user.\n:loudspeaker:: put this report on hold and get more information from the reporter.\n:x:: close this ticket with no further action.'
                  embed = discord.Embed(title="End of Report", description=end, color=0Xffc830)
                  embed.add_field(name="Take Action", value=reporter, inline=False)
                  reportdone = await reportchannel.send(embed=embed)
                  await reportdone.add_reaction('\U00002705')
                  await reportdone.add_reaction('\U0001f4e2')
                  await reportdone.add_reaction('\U0000274c')
                  await reportchannel.send("Hey <@&"+modid+">, heres a report!")
                  modchoice, user = await self.bot.wait_for('reaction_add',check=check)
                  if str(modchoice.emoji) == '\U00002705':
                      await ban()
                  if str(modchoice.emoji) == '\U0001f4e2':
                      await channel.send("A moderator will be messaging you soon for more information concerning your report on <@"+discID+">. Please wait.")
                      end = user.mention+', please message '+ctx.author.mention+' ASAP. When you are done, please close this ticket.'
                      reporter = ':white_check_mark:: to ban the reported user.\n:x:: close this ticket with no further action.'
                      embed = discord.Embed(title="Getting More Information", description=end, color=0Xffc830)
                      embed.add_field(name="Take Action", value=reporter, inline=False)
                      reportdone = await reportchannel.send(embed=embed)
                      await reportdone.add_reaction('\U00002705')
                      await reportdone.add_reaction('\U0000274c')
                      modchoice2, user = await self.bot.wait_for('reaction_add',check=check)
                      if str(modchoice2.emoji) == '\U00002705':
                          await ban()
                      else:
                          await closeReportTicket()
                  if str(modchoice.emoji) == '\U0000274c':
                      await closeReportTicket()
              else:
                  try:
                      await reportchannel.send(proof.content)
                      try:
                          async with aiohttp.ClientSession() as session:
                              async with session.get(proof.attachments[0].url) as resp:
                                  if resp.status != 200:
                                      return await channel.send('Could not download file...')
                                  data = io.BytesIO(await resp.read())
                                  await reportchannel.send(file=discord.File(data, 'proof.png'))
                      except:
                          pass
                  except:
                      async with aiohttp.ClientSession() as session:
                          async with session.get(proof.attachments[0].url) as resp:
                              if resp.status != 200:
                                  return await channel.send('Could not download file...')
                              data = io.BytesIO(await resp.read())
                              await reportchannel.send(file=discord.File(data, 'proof.png'))
                  await channel.send("Thanks, I sent that to the moderators. If thats the last piece of evidence, please type 'done' with no quotes.")
      if str(userchoice.emoji) == '2\N{variation selector-16}\N{combining enclosing keycap}': 
          await channel.send("Need support? Have some feedback for the server?\nBeing as descriptive as possible, and in only one message, please type whatever you need sent to the staff team. \nIf you need to send pictures, please do not send them to me. Say you have pictures in your message, and we will request them.")
          try:
              specialmessage = await self.bot.wait_for('message',check=lambda message: message.author == ctx.author and message.guild == None,timeout=900)
          except asyncio.TimeoutError:
              await channel.send("Timed out! Please start over with !dm")
              return
          supportchannel = await guild.create_text_channel("Support - "+author, category=category)
          await supportchannel.send("Hey <@&"+modid+"> <@&"+helperid+">, heres a support/feedback ticket!")
          suportee = 'User: '+ctx.author.mention+'\n'+str(ctx.author.id)
          content = specialmessage.content
          embed = discord.Embed(title="Support/Feedback", description=suportee, color=0Xe257fa)
          embed.add_field(name="User's Message", value=content, inline=False)
          await supportchannel.send(embed=embed)
          await channel.send("Okay, I passed that along to the staff team. They'll get back to you as soon as possible.")
          reporter = ':loudspeaker:: Get more information from the reporter.\n:x:: Close this ticket with no further action.'
          embed = discord.Embed(title="Take Action", description=reporter, color=0Xffc830)
          reportdone = await supportchannel.send(embed=embed)
          await reportdone.add_reaction('\U0001f4e2')
          await reportdone.add_reaction('\U0000274c')
          modchoice, user = await self.bot.wait_for('reaction_add',check=check)
          
          if str(modchoice.emoji) == '\U0001f4e2':
            end = user.mention+', please message '+ctx.author.mention+' ASAP. When you are done, please close this ticket.'
            reporter = ':x:: close this ticket.'
            embed = discord.Embed(title="Getting More Information", description=end, color=0Xffc830)
            embed.add_field(name="Take Action", value=reporter, inline=False)
            reportdone = await supportchannel.send(embed=embed)
            await reportdone.add_reaction('\U0000274c')
            modchoice2, user = await self.bot.wait_for('reaction_add',check=check)
            
            if str(modchoice2.emoji) == '\U0000274c':
                await closeSupportTicket()
          if str(modchoice.emoji) == '\U0000274c':
              await closeSupportTicket()
      
      if str(userchoice.emoji) == '3\N{variation selector-16}\N{combining enclosing keycap}': 
          await channel.send("Okay, I don't exactly know what you want. Being as descriptive as possible, and in only one message, please type whatever you need sent to the staff team. \nIf you need to send pictures, please do not send them to me. Say you have pictures in your message, and we will request them.")
          try:
              specialmessage = await self.bot.wait_for('message',check=lambda message: message.author == ctx.author and message.guild == None,timeout=900)
          except asyncio.TimeoutError:
              await channel.send("Timed out! Please start over with !dm")
              return
          supportchannel = await guild.create_text_channel("Other - "+author, category=category)
          await supportchannel.send("Hey <@&"+modid+"> <@&"+helperid+">, heres a wierd ticket for ya!")
          suportee = 'User: '+ctx.author.mention+'\n'+str(ctx.author.id)
          content = specialmessage.content
          embed = discord.Embed(title="Other", description=suportee, color=0X1300a6)
          embed.add_field(name="User's Message", value=content, inline=False)
          await supportchannel.send(embed=embed)
          await channel.send("Okay, I passed that along to the staff team. They'll get back to you as soon as possible.")
          reporter = ':loudspeaker:: Get more information from the reporter.\n:x:: Close this ticket with no further action.'
          embed = discord.Embed(title="Take Action", description=reporter, color=0Xffc830)
          reportdone = await supportchannel.send(embed=embed)
          await reportdone.add_reaction('\U0001f4e2')
          await reportdone.add_reaction('\U0000274c')
          modchoice, user = await self.bot.wait_for('reaction_add',check=check)
          
          if str(modchoice.emoji) == '\U0001f4e2':
            end = user.mention+', please message '+ctx.author.mention+' ASAP. When you are done, please close this ticket.'
            reporter = ':x:: close this ticket.'
            embed = discord.Embed(title="Getting More Information", description=end, color=0Xffc830)
            embed.add_field(name="Take Action", value=reporter, inline=False)
            reportdone = await supportchannel.send(embed=embed)
            await reportdone.add_reaction('\U0000274c')
            modchoice2, user = await self.bot.wait_for('reaction_add',check=check)
            
            if str(modchoice2.emoji) == '\U0000274c':
                await closeSupportTicket()
          
          if str(modchoice.emoji) == '\U0000274c':
              await closeSupportTicket()

  @commands.command(name='end')
  @commands.has_permissions(administrator=True)
  async def deleteReport(self, ctx):
    if ctx.channel.category and ctx.channel.category.name == "Reports" and ctx.channel.id != modmaillogging:
        await ctx.channel.delete()

def setup(bot):
    bot.add_cog(Modmail(bot))
