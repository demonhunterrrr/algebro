def main():
    # Importing modules
    import discord
    from discord.ext import commands
    from dotenv import load_dotenv
    from utilities import Utilities
    from stats import Stats
    from maths import Math # DO NOT NAME "maths.py" FILE "math.py"! IT WILL NOT WORK BECAUSE OF THE EXISTING LIBRARY!
    from datetime import date
    import os
    import json

    # Connecting to discord
    load_dotenv()
    nu_token = os.getenv('nu_token')
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='$',intents=intents)
    @bot.event
    async def on_ready():
        print(f"{bot.user} has connected to Discord!")
        await bot.add_cog(Utilities(bot))
        await bot.add_cog(Math(bot))

    bot.run(nu_token)

if __name__ == '__main__':
    main()
