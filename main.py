import os
import discord
import asyncio

from discord import Game
from database import Database
from datetime import datetime
from dotenv import load_dotenv
from os.path import join, dirname
from discord.ext.commands import Bot

# This is from rolley
PREFIX = '>'
DQ_CHANNEL = 'daily-coding-challenge'

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get('TOKEN')
bot = Bot(command_prefix=PREFIX)

# SQL Database Info
UNAME = os.environ.get('USERNAME')
PWD = os.environ.get('PASSWORD')

db = Database("dailybot", uname=UNAME, pwd=PWD, host="db")

# Date difference (note: checks every 12hrs)
secs = 12 * 60 * 60

# Cache stuff
user_cache = {}
question = None
question_date = None
target_channel = None


def is_mod_or_admin(author, channel_is_private=False):
    if not channel_is_private:
        perms = author.server_permissions
        if perms.manage_roles or perms.administrator:
            return True

    return db.is_admin(author.id)


def update_question():
    global question, question_date
    print("Updating Question")
    if question is None or question_date < datetime.today().date():
        question = db.get_day_question()
        question_date = datetime.today().date()


async def timer_update():
    while True:
        update_question()
        emb = get_embed()

        if target_channel is not None:
            await bot.send_message(target_channel, embed=emb)

        await asyncio.sleep(secs)


# Bot Events
@bot.event
async def on_ready():
    global db
    await bot.change_presence(game=Game(name="Hackerrank"))
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    db.start_connection()
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(timer_update(), loop=loop)


@bot.event
async def on_message(message):
    global target_channel

    if not message.channel.is_private or message.author.bot:
        # This is a passive check to update the target channel for showing question
        if target_channel is None and message.channel.name == DQ_CHANNEL:
            target_channel = message.channel

        await bot.process_commands(message)
        return

    # TODO: add check in DB to see if person is allowed to add
    if not is_mod_or_admin(message.author, channel_is_private=True):
        return

    if message.author.id in user_cache.keys():
        if message.content.upper() == 'Y' or message.content.upper() == 'YES':
            arr = user_cache[message.author.id]
            if db.add_new_question(arr[1], arr[2], arr[3]) == 1:
                await bot.send_message(message.author, "Question added.")
            else:
                await bot.send_message(message.author, "Question already in database.")
        else:
            await bot.send_message(message.author, "Question **not** added.")

        del user_cache[message.author.id]

    elif message.content.startswith("```") and message.content.endswith("```"):
        body = message.content[3:len(message.content) - 3]
        lines = body.splitlines()

        if len(lines) < 3:
            await bot.send_message(message.author, "Invalid Format. Try Again")
            return

        # index [0] is just a newline
        arr = [1, lines[1], "\n".join(lines[3:])]

        emb = get_embed(base=arr)

        await bot.send_message(message.author, embed=emb,
                               content="Type in _YES_ to keep it this way. _NO_ to try format again")

        arr.append(lines[2])
        user_cache[message.author.id] = arr
    else:
        await bot.process_commands(message)


# Bot Commands
@bot.command(name='add_admin', description='add admin to table', aliases=['aa'], brief='add new admin',
             pass_context=True)
async def add_admin(ctx):
    if len(ctx.message.mentions) == 0:
        await bot.send_message(ctx.message.channel, content='Need to supply users to add')
        return

    if not is_mod_or_admin(ctx.message.author):
        await bot.send_message(ctx.message.channel, content='You have insufficient perms to do this')
        return

    for mentioned in ctx.message.mentions:
        if db.add_admin(mentioned.id) == 0:
            await bot.send_message(ctx.message.channel, content='User {} not found'.format(mentioned.name))

    await bot.send_message(ctx.message.channel, content='Users added')


@bot.command(name='remove_admin', description='remove admin from table', aliases=['del_admin', 'da'],
             brief='delete admin', pass_context=True)
async def remove_admin(ctx):
    if len(ctx.message.mentions) == 0:
        await bot.send_message(ctx.message.channel, content='Need to supply users to add')
        return

    if not is_mod_or_admin(ctx.message.author):
        await bot.send_message(ctx.message.channel, content='You have insufficient perms to do this')
        return

    for mentioned in ctx.message.mentions:
        if db.remove_admin(mentioned.id) is None:
            await bot.send_message(ctx.message.channel, content='User {} not in table'.format(mentioned.name))

    await bot.send_message(ctx.message.channel, content='Users remove')


@bot.command(name='show_question',
             description='shows the question for the day. If a number is provided after, gets a question with that index',
             aliases=['show_q', 'q'], brief='show today\'s question', pass_context=True)
async def show_question(ctx, *args):
    global question
    if ctx.message.channel.name != DQ_CHANNEL:
        return

    if len(args) == 0:
        update_question()

        if question is None:
            emb = get_embed(base=['N/A', 'No available questions found... Contact one of channel mods!', 'N/A'])
        else:
            emb = get_embed()

        await bot.send_message(ctx.message.channel, embed=emb)
    else:
        try:
            succ = db.get_index_question(int(args[0]))

            if succ is not None:
                emb = get_embed(base=succ)
                await bot.send_message(ctx.message.channel, embed=emb)
            else:
                await bot.send_message(ctx.message.channel, content="could not find question with supplied index")
        except ValueError:
            await bot.send_message(ctx.message.channel, content="Please supply **A NUMBER**")


@bot.command(name='list_questions', description='lists all questions from index provided', aliases=['list', 'lq'],
             brief='list all questions', pass_context=True)
async def list_questions(ctx, *args):
    global db
    if len(args) == 0:
        string = db.list_questions()
    else:
        try:
            string = db.list_questions(first_index=int(args[0]))
        except ValueError:
            string = db.list_questions()

    string = '```' + string + '```'

    await bot.send_message(ctx.message.channel, content=string)


@bot.command(name='remove_question', description='deletes question based on index, found by using >list',
             aliases=['del', 'remove'],
             brief='delete question on index', pass_context=True)
async def remove_question(ctx, *args):
    if not is_mod_or_admin(ctx.message.author):
        await bot.send_message(ctx.message.channel, content="You have insufficient perms to do this")
        return

    global db, question
    if len(args) == 0:
        await bot.send_message(ctx.message.channel, content="Please supply index to delete")
        return

    try:
        succ = db.remove_question(int(args[0]))

        if succ is not None:
            if question == succ:
                question = None
            await bot.send_message(ctx.message.channel, content="Successfully deleted")
        else:
            await bot.send_message(ctx.message.channel, content="could not find question with supplied index")
    except ValueError:
        await bot.send_message(ctx.message.channel, content="Please supply **A NUMBER**")


def get_embed(base=None):
    global question

    if base is None:
        question_text = "[ *{}* ] Asked by **{}**\n\n{}".format(question[0], question[1], question[2])

        if len(question) == 4:
            question_text + "\nLeetcode link: {}".format(question[3])
    else:
        question_text = "[ *{}* ] Asked by **{}**\n\n{}".format(base[0], base[1], base[2])

    return discord.Embed(title='Question for **{}**'.format(datetime.today().date()), type='rich',
                         description=question_text, color=0xffd700)


if __name__ == '__main__':
    bot.run(TOKEN)
