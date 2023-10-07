import discord
import asyncio
from discord.ext import commands
from env_secrets import get_token
from datetime import datetime

dev_token = ""
footer_msg = f"Trivskins Bot v3.0 | Last updated: {datetime.now().strftime('%x at %X')}"
intents = discord.Intents.all()
intents.members = True

startup_extensions = ["cogs.util_commands", "cogs.util"]

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")


async def main():
    async with bot:
        for extension in startup_extensions:
            try:
                await bot.load_extension(extension)
            except Exception as e:
                print(e)
        await bot.start(get_token())
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

if __name__ == "__main__":
    asyncio.run(main())
