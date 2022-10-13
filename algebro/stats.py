from discord.ext import commands
from datetime import date
from utils import id_from_mention
import json


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add_word', help='Add either a bad or good word to the lists.')
    async def add_word(self, ctx, value: str, word: str):
        if value != "bad" and value != "good":
            await ctx.send(f'You can only enter "bad" or "good" words, not {value} words!')
            return

        with open('words.json', 'r+') as f:
            words = json.load(f)
            if word in words['bad'] or word in words['good']:
                await ctx.send(f'{word} is already a {list(words.keys())[list(words.values()).index(word)]} word!')
            words[value].append(word)
            f.seek(0)
            json.dump(words, f, indent=4, default=str)
            await ctx.send(f'Added {word} to {value} words!')

    @commands.command(name='list_words', help='List the bad or good words')
    async def list_words(self, ctx):
        with open('words.json', 'r+') as f:
            words = json.load(f)
            bads = '\n'.join(words["bad"])
            goods = '\n'.join(words["good"])
            await ctx.send(f'```Bad Words:\n{bads}\n\nGood Words:\n{goods}```')

    @commands.command(name='swear_score', help='See someone else\'s swear score')
    async def swear_score(self, ctx, person):
        with open('users.json', 'r+') as f:
            users = json.load(f)
            try:
                await ctx.send(f'{person} has a swear score of {users[id_from_mention(person)][2]}!')
            except KeyError:
                await ctx.send(f'That user either does not exist or hasn\'t sent a message in the server yet.')

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('users.json', 'r+') as f:
            users = json.load(f)
            if str(message.author.id) in users:
                users[str(message.author.id)][3] = message.author.name
            else:
                users[str(message.author.id)] = [0, 0, 0, message.author.name]
            with open('words.json', 'r+') as word_json:
                words = json.load(word_json)
                for i in words['bad']:
                    users[str(message.author.id)][2] += 1 if i in message.content else 0
                for i in words['good']:
                    users[str(message.author.id)][2] -= 1 if i in message.content else 0
            f.seek(0)
            json.dump(users, f, indent=4)

        with open('messages.json', 'r+') as f:
            messages = json.load(f)
            messages.append({'content': message.content, 'author': message.author.name, 'date': date.today()})
            f.seek(0)
            json.dump(messages, f, indent=4, default=str)
