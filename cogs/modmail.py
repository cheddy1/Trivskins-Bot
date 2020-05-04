import discord
import io
import aiohttp

from discord.ext import commands

serverid = #guild id
modmail = #modmail category id
modid= #mod role id
modmaillogging = #modmail logging id


class Modmail(commands.Cog, name="Modmail Function"):
  def __init__(self, bot):
        self.bot = bot

  @commands.command(name='dm')
  async def sendDM(self, ctx):
      guild = ctx.message.guild
      if guild == None:
          guild = self.bot.get_guild(serverid)
      category = guild.get_channel(modmail) 
      modmailloggingchannel =  guild.get_channel(modmaillogging)
      channel = await ctx.author.create_dm()
      author = str(ctx.author)
      def check(reaction, user):
          return user.id != self.bot.user.id
      def checkUser(reaction, user):
          return user.id != self.bot.user.id and user.id == ctx.author.id
      await channel.send("Hey, what can I help you with?\n\n**1.** Report another user.\n**2.** Trading help.\n**3.** Discord support/feedback.\n**4.** Other\n\nPlease respond with your choice of 1-4.")
      answer = await self.bot.wait_for('message',check=lambda message: message.author == ctx.author and message.guild == None)
      
      if answer.content == '1':
          await channel.send('What reason are you reporting for?\n\n**1.** Scamming\n**2.** Advertising\n**3.** Discord TOS Break\n**4.** Other\n\nPlease respond with your choice of 1-4.')
          reportreason = await self.bot.wait_for('message',check=lambda message: message.author == ctx.author and message.guild == None)
          if reportreason.content == '1':
              reason = 'Scamming'
          if reportreason.content == '2':
              reason = 'Advertising'
          if reportreason.content == '3':
              reason = 'Discord TOS Break'
          if reportreason.content == '4':
              reason = 'Other'
          await channel.send("Okay, let's report a user for "+reason+". Please send me their discord user ID. If you do not know how to find it, please visit here: <https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID->")
          discID = await self.bot.wait_for('message',check=lambda message: message.author == ctx.author and message.guild == None)
          reportchannel = await guild.create_text_channel("Report - "+author, category=category)
          reportchannel
          await reportchannel.send("Hey <@&"+modid+">, heres a report!")
          desc = "Reason: "+reason
          reportee = 'Name: <@'+discID.content+'>\nDiscord ID: '+discID.content
          reporter = 'Name: '+ctx.author.mention+'\nDiscord ID: '+str(ctx.author.id)
          embed = discord.Embed(title="Report", description=desc, color=0Xfc2d2d)
          embed.add_field(name="User Being Reported", value=reportee, inline=True)
          embed.add_field(name="User Reporting", value=reporter, inline=True)
          await reportchannel.send(embed=embed)
          await channel.send("Now, please send all available proof to me, and I'll relay it to the moderators. Please type 'done' without the quotes once you are done sending the proof.")
          done = False
          while done == False:
              proof = await self.bot.wait_for('message',check=lambda message: message.author == ctx.author and message.guild == None)
              if proof.content == 'done':
                  done = True
                  end = ctx.author.mention+' has indicated the end of the report.'
                  reporter = ':white_check_mark:: to ban the reported user.\n:loudspeaker:: put this report on hold and get more information from the reporter.\n:x:: close this ticket with no further action.'
                  embed = discord.Embed(title="End of Report", description=end, color=0Xffc830)
                  embed.add_field(name="Take Action", value=reporter, inline=False)
                  reportdone = await reportchannel.send(embed=embed)
                  await reportdone.add_reaction('\U00002705')
                  await reportdone.add_reaction('\U0001f4e2')
                  await reportdone.add_reaction('\U0000274c')
                  modchoice, user = await self.bot.wait_for('reaction_add',check=check)
                  if str(modchoice.emoji) == '\U00002705':
                      await channel.send("Thanks for the report, "+ctx.author.mention+', the user you reported was banned, and the ticket has been closed. If you would like open a new one, just send me a message.')
                      desc = "User Banned\nReason: **"+reason+"**"
                      reportee = '<@'+discID.content+'>\nDiscord ID: '+discID.content
                      reporter = ctx.author.mention+'\nDiscord ID: '+str(ctx.author.id)
                      moderator = '<@'+str(user.id)+'>\nDiscord ID: '+str(user.id)
                      embed = discord.Embed(title="Report Ticket Closed", description=desc, color=0Xfc2d2d)
                      embed.add_field(name="User Banned", value=reportee, inline=True)
                      embed.add_field(name="Reporter", value=reporter, inline=True)
                      embed.add_field(name="Moderator", value=moderator, inline=True)
                      await modmailloggingchannel.send(embed=embed)
                      await guild.ban(discord.Object(id=int(discID.content)),reason=reason, delete_message_days=7)
                      await reportchannel.delete()
                  if str(modchoice.emoji) == '\U0001f4e2':
                      await channel.send("A moderator will be messaging you soon for more information concerning your report on <@"+discID.content+">. Please wait.")
                      end = user.mention+', please message the user ASAP. When you are done, please close this ticket with one of two options.'
                      reporter = ':white_check_mark:: to ban the reported user.\n:x:: close this ticket with no further action.'
                      embed = discord.Embed(title="Getting More Information", description=end, color=0Xffc830)
                      embed.add_field(name="Take Action", value=reporter, inline=False)
                      reportdone = await reportchannel.send(embed=embed)
                      await reportdone.add_reaction('\U00002705')
                      await reportdone.add_reaction('\U0000274c')
                      modchoice2, user = await self.bot.wait_for('reaction_add',check=check)
                      if str(modchoice2.emoji) == '\U00002705':
                          await channel.send("Thanks for the report, "+ctx.author.mention+', the user you reported was banned, and the ticket has been closed. If you would like open a new one, just send me a message.')
                          desc = "User Banned\nReason: **"+reason+"**"
                          reportee = '<@'+discID.content+'>\nDiscord ID: '+discID.content
                          reporter = ctx.author.mention+'\nDiscord ID: '+str(ctx.author.id)
                          moderator = '<@'+str(user.id)+'>\nDiscord ID: '+str(user.id)
                          embed = discord.Embed(title="Report Ticket Closed", description=desc, color=0Xfc2d2d)
                          embed.add_field(name="User Banned", value=reportee, inline=True)
                          embed.add_field(name="Reporter", value=reporter, inline=True)
                          embed.add_field(name="Moderator", value=moderator, inline=True)
                          await modmailloggingchannel.send(embed=embed)
                          await guild.ban(discord.Object(id=int(discID.content)),reason=reason, delete_message_days=7)
                          await reportchannel.delete()
                      else:
                          end = user.mention+', please type the reason why you are closing the ticket. For example, \"No action is needed\" or \"Issue resolved\" and I\'ll close the ticket.'
                          embed = discord.Embed(title="Closing Ticket", description=end, color=0Xed9632)
                          await reportchannel.send(embed=embed)
                          closereason = await self.bot.wait_for('message',check=lambda message: message.channel == reportchannel and message.author.id != self.bot.user.id)
                          desc = "\nReason Reported: "+reason+"\nReason Closed: "+closereason.content
                          reportee = '<@'+discID.content+'>\nDiscord ID: '+discID.content
                          reporter = ctx.author.mention+'\nDiscord ID: '+str(ctx.author.id)
                          moderator = '<@'+str(user.id)+'>\nDiscord ID: '+str(user.id)
                          embed = discord.Embed(title="Report Ticket Closed", description=desc, color=0Xfc8686)
                          embed.add_field(name="User Reported", value=reportee, inline=True)
                          embed.add_field(name="Reporter", value=reporter, inline=True)
                          embed.add_field(name="Moderator", value=moderator, inline=True)
                          await modmailloggingchannel.send(embed=embed)
                          await reportchannel.delete()
                  if str(modchoice.emoji) == '\U0000274c':
                      end = user.mention+', please type the reason why you are closing the ticket. For example, \"No action is needed\" or \"Issue resolved\" and I\'ll close the ticket.'
                      embed = discord.Embed(title="Closing Ticket", description=end, color=0Xed9632)
                      await reportchannel.send(embed=embed)
                      closereason = await self.bot.wait_for('message',check=lambda message: message.channel == reportchannel and message.author.id != self.bot.user.id)
                      desc = "\nReason Reported: "+reason+"\nReason Closed: "+closereason.content
                      reportee = '<@'+discID.content+'>\nDiscord ID: '+discID.content
                      reporter = ctx.author.mention+'\nDiscord ID: '+str(ctx.author.id)
                      moderator = '<@'+str(user.id)+'>\nDiscord ID: '+str(user.id)
                      embed = discord.Embed(title="Report Ticket Closed", description=desc, color=0Xfc8686)
                      embed.add_field(name="User Reported", value=reportee, inline=True)
                      embed.add_field(name="Reporter", value=reporter, inline=True)
                      embed.add_field(name="Moderator", value=moderator, inline=True)
                      await modmailloggingchannel.send(embed=embed)
                      await reportchannel.delete()
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


  @commands.command(name='end')
  async def deleteReport(self, ctx):
    if ctx.channel.category and ctx.channel.category.name == "Reports":
        await ctx.channel.delete()



def setup(bot):
    bot.add_cog(Modmail(bot))
