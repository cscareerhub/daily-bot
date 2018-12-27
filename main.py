import os

from discord import Game
from dotenv import load_dotenv
from os.path import join, dirname
from database import Database
from discord.ext.commands import Bot

# This is from rolley
cmd_prefix = '>'
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get('TOKEN')
bot = Bot(cmd_prefix)

# SQL Database Info
UNAME = os.environ.get('USERNAME')
PWD = os.environ.get('PASSWORD')

db = Database("daily_bot")

user_cache = {}


# Bot events
@bot.event
async def on_ready():
    await bot.change_presence(game=Game(name="Hackerrank"))
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.event
async def on_message(message):
    if not message.channel.is_private:
        return

    # TODO: add check in DB to see if person is allowed to add

    if message.author.id in user_cache.keys():
        if message.content.upper() == 'Y' or message.content.upper() == 'YES':
            if db.add_new_question(user_cache[message.author.id]) == 1:
                await bot.send_message(message.author, "Question added.")
            else:
                await bot.send_message(message.author, "Question already in database.")
        else:
            await bot.send_message(message.author, "Question **not** added.")

        del user_cache[message.author.id]

    elif message.content.startswith("```") and message.content.endswith("```"):
        body = message.content[3:len(message.content) - 3]
        await bot.send_message(message.author,
                               "```{}```\nType in _YES_ to keep it this way. _NO_ to try format again".format(body))
        user_cache[message.author.id] = body


if __name__ == '__main__':
    bot.run(TOKEN)
