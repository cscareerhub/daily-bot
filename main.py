import os
import discord

from discord import Game
from threading import Timer
from database import Database
from datetime import datetime
from dotenv import load_dotenv
from os.path import join, dirname
from discord.ext.commands import Bot

# This is from rolley
PREFIX = '!'
DQ_CHANNEL = 'daily-coding-challenge'

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get('TOKEN')
bot = Bot(command_prefix=PREFIX)

# SQL Database Info
UNAME = os.environ.get('USERNAME')
PWD = os.environ.get('PASSWORD')

db = Database("daily_bot")

# Date difference (all from SO)
x = datetime.today()
y = x.replace(day=x.day + 1, hour=1, minute=0, second=0, microsecond=0)
delta_t = y - x
secs = delta_t.seconds + 1

# Cache stuff
user_cache = {}
question = None
question_date = None


def update_question():
    global question, question_date
    print("Updating Question")
    if question is None or question_date < datetime.today().date():
        question = db.get_day_question()
        question_date = datetime.today().date()


timer = Timer(secs, update_question)


# Bot Events
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
        await bot.process_commands(message)
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
    else:
        await bot.process_commands(message)


# Bot Commands
@bot.command(name='show_question', description='shows the question for the day', aliases=['show_q', 'q'],
             brief='show today\'s question', pass_context=True)
async def show_question(ctx):
    global question
    if ctx.message.channel.name != DQ_CHANNEL:
        return

    if question is None:
        update_question()

    emb = discord.Embed(title='Question for **{}**'.format(datetime.today().date()), type='rich',
                        description=question, color=0xffd700)
    await bot.send_message(ctx.message.channel, embed=emb)


if __name__ == '__main__':
    timer.start()
    bot.run(TOKEN)
