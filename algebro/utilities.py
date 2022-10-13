from discord.ext import commands
import random
import json

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll", help="roles a dice with <sides> sides.")
    async def roll(self, ctx, sides: int):
        await ctx.send(f'The dice rolled...  a {random.randint(1, sides)}!')

    @commands.command(name="coinflip", help="Flips a coin <flips> times.")
    async def coinflip(self, ctx, flips: int):
        flips_list = [random.randint(0, 1) for i in range(flips)]
        await ctx.send(f'The coin flipped {flips} times and it mostly landed on... ' +
                       f'{"heads!" if flips_list.count(0) > flips / 2 else "tails!"}')
        await ctx.send(f'Specifically, it landed on heads {flips_list.count(0)} times, ' +
                       f'and tails {flips_list.count(1)} times')
