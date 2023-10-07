# This cog provides some general usage commands. At some point, I'd like
# to add a functionality that allows to create more commands from inside
# the server itself and stores them.

import discord
from discord.ext import commands
from discord import app_commands
from main import footer_msg


class Util_Commands(commands.Cog, name="General Commands"):
    def __init__(self, bot):
        self.bot = bot

    # Pulls up an invite link
    @app_commands.command(description="Get an invite link!")
    async def invite(self, interaction: discord.Interaction):
        await interaction.response.send_message("https://discord.gg/NfpThYWgRt")

    # Pulls up an invite link
    @app_commands.command(description="Learn about the bot!")
    async def about(self, interaction: discord.Interaction):
        desc = "This bot is undergoing a major rewrite. Please check back for new features!"
        contribute = "Want to help contribute? DM <@217440011451105280>!"
        embed = discord.Embed(
            title="About Trivskins Trading",
            description=desc,
            color=0x2C3675,
        )
        embed.add_field(name="Contribute to the Bot", value=contribute, inline=False)
        embed.set_footer(text=footer_msg)
        await interaction.response.send_message(embed=embed)

    # Alerts a user about modmail
    @commands.command(name="modmail")
    async def modmail(self, ctx):
        await ctx.message.delete()
        mention = ctx.message.content.replace("!modmail", "")
        await ctx.message.channel.send(
            "Need to report someone, provide feedback, or get support, "
            + mention
            + "? Open a modmail with **!dm**"
        )

    # General help command
    @app_commands.command(description="Load this help menu.")
    async def help(self, interaction: discord.Interaction):
        cmds = commands.Cog.get_app_commands(self)
        command_list = ""
        for command in cmds:
            description = command.description.partition("\n")[0]
            command_list += f"</{command.name}:{command.id}> - *{description}*\n"
        desc = "Have a more specific question? Reach out to the staff team at any time."
        general = command_list
        embed = discord.Embed(
            title="Trivskins Trading Bot Help",
            description=desc,
            color=0x2C3675,
        )
        embed.add_field(name="General Commands:", value=general, inline=False)
        embed.set_footer(text=footer_msg)
        await interaction.response.send_message(embed=embed)

    # Recognizes supporters. At some point, would like to add an ability to add
    # supporters from the server.
    @app_commands.command(description="How can you support?")
    async def support(self, interaction: discord.Interaction):
        desc = "Help support the development of the Trivskins Trading server and bot. Click on the link above if you're interested!"
        staff = "Want to support another way? Help make this server a better place and join the staff team! DM <@217440011451105280> to learn more."
        supporters = "Thank you to anyone who supports the bot, the website, and this server. Donating any amount will get your name below, a royal purple chat role, and future supporter only betas and bot features! \n\n**Argarest**\n**ÅRRØ**"
        embed = discord.Embed(
            title="Support!",
            description=desc,
            url="https://www.paypal.me/cheddy",
            color=0xAC27FD,
        )
        embed.add_field(name="Join the Staff Team!", value=staff, inline=False)
        embed.add_field(name="Supporters", value=supporters, inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Util_Commands(bot))
