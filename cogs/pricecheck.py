import discord
import aiohttp
from discord.ext import commands
import json
import difflib
import asyncio

priceCheckChannel = 


class PriceCheck(commands.Cog, name="Price check command"):
    def __init__(self, bot):
        self.bot = bot

        # Hold data so we don't have to reread the jsons every time
        self.all_skins_data = {}
        self.list_of_items = ['']

        # Load them at startup
        try:
            with open('csgo_item_data.json', 'r') as temp_file:
                self.all_skins_data = json.load(temp_file)
            with open('csgo_item_list.json', 'r') as temp_file:
                self.list_of_items = json.load(temp_file)
        except Exception as e:
            print(str(e))

    # Runs when the bot is first started up
    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(priceCheckChannel)

        # Refresh the skin list every week
        while True:

            # Retrieve a json with all items in CS:GO
            async with aiohttp.ClientSession() as session:
                async with session.get('http://csgobackpack.net/api/GetItemsList/v2/') as resp:
                    resp = await resp.text()
                    temp_json = json.loads(resp)

                    # Only overwrite allSkinsData if tempJson has the correct data
                    # listOfItems is a list of the keys in that dict (which are item names)
                    if temp_json['success']:
                        with open('csgo_item_data.json', 'w') as temp_file:
                            self.all_skins_data = temp_json
                            json.dump(temp_json, temp_file)
                        with open('csgo_item_list.json', 'w') as temp_file:
                            list_of_items = list(temp_json['items_list'].keys())
                            self.list_of_items = list_of_items
                            json.dump(list_of_items, temp_file)
                        await channel.send("CS:GO skins and prices refreshed.")
                        await asyncio.sleep(604800)

                    else:
                        await channel.send("Could not reload the item list. Is CSGO Backpack down?")
                        await asyncio.sleep(604800)

    # CSGO skin market price skin checker command
    @commands.command(name='pc')
    async def pc(self, ctx, *args):
        async with ctx.typing():
            skin_name = ' '.join(args)

            # If the user doesn't input a skin, tell them
            if skin_name == "":
                return await ctx.send('!pc cannot be empty, ' + ctx.message.author.mention + '. Type !pc help to get started!')

            else:
                
                # This should never happen, but if the skin list is empty, it needs to be reloaded
                if not self.list_of_items:
                    await ctx.send("Please wait for the list of skins to load!")

                else:
                    # From the users input, try to guess what item they're trying to check
                    raw_skin_name = difflib.get_close_matches(skin_name.title(), self.list_of_items, 1, .4)

                    # This happens if the user does not input a skin close enough to the correct one
                    if not raw_skin_name:
                        await ctx.send("No results. Please try again or ping <@217440011451105280> if you have any issues.")

                    else:
                        raw_skin_name = str(raw_skin_name[0])
                        requested_skin_data = self.all_skins_data['items_list'][raw_skin_name]

                        # Get all the data points from the dict
                        color = int(hex(int(requested_skin_data['rarity_color'], 16)), 16)
                        requested_skin_data_price = requested_skin_data['price']['30_days']
                        average_price = str(requested_skin_data_price['average'])
                        lowest_price = str(requested_skin_data_price['lowest_price'])
                        highest_price = str(requested_skin_data_price['highest_price'])
                        amount_sold = str(requested_skin_data_price['sold'])

                        # Get the URLs for the embed
                        skin_icon = "http://cdn.steamcommunity.com/economy/image/" + str(
                            requested_skin_data['icon_url'] + "/")
                        steam_link = ('https://steamcommunity.com/market/listings/730/' + raw_skin_name.replace(')', '%29')).replace(' ', '%20')
                        bitskins_link = ('https://bitskins.com/?app_id=730&market_hash_name=' + raw_skin_name.replace(')', '%29')).replace(' ', '%20')

                        # Define the embed and print it
                        desc = 'The average price for \n' + '**' + raw_skin_name + '** is: **$' + average_price + '**\n\nAmount sold: **' + amount_sold + '**\nLowest price sold for: **$' + lowest_price + '**\nHighest price sold for: **$' + highest_price + '**'
                        embed = discord.Embed(title="Price Check", description=desc, url=skin_icon, color=color)
                        links = "[Steam Market](" + steam_link + ")\n[Bitskins](" + bitskins_link + ")\n_ _"
                        embed.add_field(name="Links", value=links, inline=False)
                        embed.set_thumbnail(url=skin_icon)
                        embed.set_footer(text="All data is from the steam marketplace from the past 30 days", icon_url="https://cdn.discordapp.com/avatars/217440011451105280/7752b9953c981fe9b072dd0949e956f4.png?size=128")
                        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(PriceCheck(bot))
