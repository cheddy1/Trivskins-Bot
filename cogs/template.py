# This cog forces users who are posting in trading channels to follow
# predetermined templates to keep all trading ads consistant and neat.
# It also removes any ads with certain words not allowed by the server.

from discord.ext import commands
import discord
import re

from env_secrets import get_guild_id

# Channel names for the bot to check for/use
trade_logging = "🌳︱trading-logging"
low_high_tier_channels = ["💲︱low-tier", "💲︱high-tier"]
steam_channel_list = [
    "💲︱low-tier",
    "💲︱high-tier",
    "💲︱knife-gloves",
    "💲︱tf2",
    "💲︱dota2",
]
trade_template = "📄︱trading-template"


# Class declaration
class Template(commands.Cog, name="Ad Template Checker"):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(get_guild_id())

        if guild is not None:
            logging = discord.utils.get(guild.text_channels, name=trade_logging)
            if logging is not None:
                self.logging = logging
            template = discord.utils.get(guild.text_channels, name=trade_template)
            if template is not None:
                self.template_id = template.id

    # Makes sure the user is not spamming the channel by checking who was the last one to post
    # Returns true if the user isn't spamming
    async def check_spam(self, ctx):
        fetch_id = [user async for user in ctx.channel.history(limit=2)]
        if fetch_id[1].author != ctx.author and ctx.author.id != 217440011451105280:
            await ctx.delete()
            await self.logging.send(
                f"{ctx.author.mention}, please wait until someone else posts an ad before posting yours again. Please refer to <#{self.template_id}> for our rules.\n"
            )
            return False
        return True

    # Make sure a user hasn't used any of the banned words in their ad
    # Returns True if the user doesnt have any banned words
    async def check_for_banned_words(self, ctx) -> bool:
        banned_list = [
            "cash",
            "paypal",
            "steam card",
            "gift card",
            "bitcoin",
            "btc",
            "crypto",
            "steam gift card",
            "alipay",
            "bank transfer",
            "eth",
            "qq",
            "dollar",
            "usd",
            "euro",
        ]
        any_violations = re.findall(
            r"(?=\b(" + "|".join(banned_list) + r")\b)", ctx.content.lower()
        )
        if any_violations:
            volition = ", ".join(any_violations)
            await self.logging.send(
                f"Sorry {ctx.author.mention}, but your ad included banned word(s) or phrase(s). You said **{volition}** which is currently not allowed according to our rules. \nPlease refer to the list of banned words and phrases in <#{trade_template}> before posting again.\n"
            )
            await ctx.delete()
            return False
        else:
            return True

    # React on any message sent
    @commands.Cog.listener()
    async def on_message(self, ctx):
        # Ignore if in a dm message or if its the bot
        guild = ctx.guild
        if guild == None or ctx.author.bot:
            return

        # Steam based game channels
        if ctx.channel.name in steam_channel_list:
            if await self.check_for_banned_words(ctx) and await self.check_spam(ctx):
                if (
                    ("[H]" not in ctx.content)
                    or ("[W]" not in ctx.content)
                    or (
                        ("steamcommunity.com/tradeoffer" not in ctx.content)
                        and ("[TL]" not in ctx.content)
                    )
                ):
                    await self.logging.send(
                        f"Sorry {ctx.author.mention}, but your trade ad didn't follow our required template, and therefore deleted. Please refer to <#{self.template_id}> before posting again.\n"
                    )
                    await ctx.delete()
                else:
                    # If the ad passes all other checks, make sure that the ad does not have a knife in the incorrect channel
                    if ctx.channel.name in low_high_tier_channels:
                        ad = ctx.content.lower()
                        if (
                            (ad.find("knife") < ad.find("[w]") and ad.find("knife") > 0)
                            or (ad.find("daggers") < ad.find("[w]") and ad.find("daggers") > 0)
                            or (ad.find("bayonet") < ad.find("[w]") and ad.find("bayonet") > 0)
                            or (ad.find("karambit") < ad.find("[w]") and ad.find("karambit") > 0)
                            or (ad.find("glove") < ad.find("[w]") and ad.find("glove") > 0)
                        ):
                            await self.logging.send(
                                "Bad puppy, "
                                + ctx.author.mention
                                + "! Looks like you had a knife/glove in your **[H]** block. Please post the knife/glove as a separate ad in <#556875284574371871>.\n"
                            )
                            await ctx.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(Template(bot))
