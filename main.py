import logging
import discord
import asyncio
from discord.ext import commands
from env_secrets import get_environment_info, get_guild_id

env_info = get_environment_info()
intents = discord.Intents.all()
intents.members = True

startup_extensions = ["cogs.util_commands", "cogs.util", "cogs.template"]

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
discord.utils.setup_logging(handler=handler, level=env_info["logging_level"])


@bot.event
async def on_ready():
    print(f"bot logged as {bot.user}")


@bot.command()
async def sync(ctx):
    if ctx.author.id == 217440011451105280:
        cmds = await bot.tree.sync()
        for cmd in cmds:
            bot.tree._global_commands[cmd.name].id = cmd.id
        await ctx.send("Command tree synced.")
    else:
        await ctx.send("You must be the owner to use this command!")


# async def main():
#     async with bot:
#         for cog in os.listdir("./cogs"):
#             if cog.endswith(".py"):
#                 await bot.load_extension(f"cmds.{cog[:-3]}")
#         await bot.start(prod_secret)


async def load_extensions():
    for extension in startup_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(e)


async def start_up():
    async with bot:
        await load_extensions()
        await bot.start(token=env_info["token"])


asyncio.run(start_up())
