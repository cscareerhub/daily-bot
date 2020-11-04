import os
import json
import discord
import asyncio

from discord import Game, DMChannel

from database import Database
from datetime import datetime
from dotenv import load_dotenv
from os.path import join, dirname
from input_parser import json_parser
from discord.ext.commands import Bot

PREFIX = '>'
DQ_CHANNEL = 'daily-coding-challenge'
Q_CHANNEL = 'programming-challenges'

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

editor_cache = {}


def update_question():
    global question, question_date
    print("Updating Question")
    if question is None or question_date < datetime.today().date():
        question = db.get_day_question()
        question_date = datetime.today().date()


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


async def timer_update():
    global target_channel

    while True:
        update_question()
        emb = get_embed()

        if target_channel is not None:
            await target_channel.send(embed=emb)

        await asyncio.sleep(secs)


def is_mod_or_admin(author, channel, channel_is_private=False):
    global db
    if not channel_is_private:
        perms = author.permissions_in(channel)
        if perms.manage_roles or perms.administrator:
            return True

    return db.is_admin(author.id)


# Bot Events
@bot.event
async def on_ready():
    global db
    await bot.change_presence(activity=Game(name="Hackerrank"))
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

    if not isinstance(message.channel, DMChannel) or message.author.bot:
        # This is a passive check to update the target channel for showing question
        if target_channel is None and message.channel.name == DQ_CHANNEL:
            target_channel = message.channel

        await bot.process_commands(message)
        return

    if not is_mod_or_admin(message.author, message.channel, channel_is_private=True):
        return

    if len(message.attachments) == 1:
        file_url = message.attachments[0]['url']

        if file_url.endswith(".json"):
            await message.channel.send("Attempting to add bulk question list")
            question_list = json_parser(file_url)
            db.add_multiple_questions(question_list)
            await message.channel.send("Added questions in bulk")
            return
        else:
            await message.channel.send("I only support JSON files right now")
            return

    if message.author.id in user_cache.keys():
        if message.content.upper() == 'Y' or message.content.upper() == 'YES':
            arr = user_cache[message.author.id]
            if db.add_new_question(arr[1], arr[2], arr[3]) == 1:
                await message.channel.send("Question added.")
            else:
                await message.channel.send("Question already in database.")
        else:
            await message.channel.send("Question **not** added.")

        del user_cache[message.author.id]

    elif message.content.startswith("```") and message.content.endswith("```"):
        body = message.content[3:len(message.content) - 3]
        lines = body.splitlines()

        if message.author.id in editor_cache.keys():
            if update_question_details(message, message.author.id):
                await message.channel.send(content="Question has been updated")
            else:
                await message.channel.send(content="Question could not be updated, try again")
            return

        if len(lines) < 3:
            await message.channel.send("Invalid Format. Try Again")
            return

        # index [0] is just a newline
        arr = [1, lines[1], "\n".join(lines[3:])]

        emb = get_embed(base=arr)

        await message.channel.send(embed=emb, content="Type in _YES_ to keep it this way. _NO_ to try format again")

        arr.append(lines[2])
        user_cache[message.author.id] = arr
    else:
        await bot.process_commands(message)


def update_question_details(msg, author_id):
    global question

    q = msg.content[3:len(msg.content) - 3]
    index = editor_cache[author_id]

    del editor_cache[author_id]
    result = db.modify_question(index, q)

    if question[0] == index and result:
        question = db.get_day_question()

    return result


# Bot Commands
@bot.command(name='add_admin', description='add admin to table', aliases=['aa'], brief='add new admin',
             pass_context=True)
async def add_admin(ctx):
    if len(ctx.message.mentions) == 0:
        await ctx.message.channel.send('Need to supply users to add')
        return

    if not is_mod_or_admin(ctx.message.author, ctx.message.channel):
        await ctx.message.channel.send(content='You have insufficient perms to do this')
        return

    for mentioned in ctx.message.mentions:
        if db.add_admin(mentioned.id) == 0:
            await ctx.message.channel.send(content='User {} not found'.format(mentioned.name))

    await ctx.message.channel.send(content='Users added')


@bot.command(name='remove_admin', description='remove admin from table', aliases=['del_admin', 'da'],
             brief='delete admin', pass_context=True)
async def remove_admin(ctx):
    if len(ctx.message.mentions) == 0:
        await ctx.message.channel.send(content='Need to supply users to add')
        return

    if not is_mod_or_admin(ctx.message.author, ctx.message.channel):
        await ctx.message.channel.send(content='You have insufficient perms to do this')
        return

    for mentioned in ctx.message.mentions:
        if db.remove_admin(mentioned.id) is None:
            await ctx.message.channel.send(content='User {} not in table'.format(mentioned.name))

    await ctx.message.channel.send(content='Users removed')


@bot.command(name='edit_question', description='edits a question', aliases=['edit'], brief='update question',
             pass_context=True)
async def edit_question(ctx, *args):
    if not is_mod_or_admin(ctx.message.author, ctx.message.channel):
        await ctx.message.channel.send(content="You have insufficient perms to do this")
        return

    if len(args) == 0:
        await ctx.message.channel.send(content="You need to specify a number...")
        return

    try:
        index = int(args[0])
        editor_cache[ctx.message.author.id] = index
        await ctx.message.channel.send(content="Please enter the question body surrounded by triple backticks")
    except ValueError:
        await ctx.message.channel.send(content="A number, y'know like 0, or 1, or 1997. This isn't that hard")


@bot.command(name='sample_json', description='show sample of json for input purposes', aliases=['sj', 'json'],
             brief='json file sample', pass_context=True)
async def sample_json_format(ctx):
    questions = []

    for i in range(3):
        q = db.get_random_question()
        questions.append({"title": q[1], "body": q[2], "ds": "N/A"})
        
    parsed_to_json = json.dumps(questions)

    await ctx.message.channel.send("```"+parsed_to_json+"```")


@bot.command(name='show_question',
             description='shows the question for the day. If a number is provided after, gets a question with that index',
             aliases=['show_q', 'q'], brief='show today\'s question', pass_context=True)
async def show_question(ctx, *args):
    global question

    if len(args) == 0:
        if ctx.message.channel.name != DQ_CHANNEL:
            return

        update_question()

        if question is None:
            emb = get_embed(base=['N/A', 'No available questions found... Contact one of channel mods!', 'N/A'])
        else:
            emb = get_embed()

        await ctx.message.channel.send(embed=emb)
    else:
        if ctx.message.channel.name != Q_CHANNEL:
            return

        try:
            succ = db.get_index_question(int(args[0]))

            if succ is not None:
                emb = get_embed(base=succ)
                await ctx.message.channel.send(embed=emb)
            else:
                await ctx.message.channel.send(content="could not find question with supplied index")
        except ValueError:
            await ctx.message.channel.send(content="Please supply **A NUMBER**")


@bot.command(name='random_question', aliases=['random', 'rq'], brief='get random question from database',
             description='gets a random question from the database. Questions can repeat', pass_context=True)
async def random_question(ctx, *args):
    if ctx.message.channel.name != Q_CHANNEL:
        return

    if len(args) == 0:
        emb = get_embed(db.get_random_question())
    else:
        emb = get_embed(db.get_random_question(company=args[0]))

    await ctx.message.channel.send(embed=emb)


@bot.command(name='list_questions', description='lists all questions from index provided', aliases=['list', 'lq'],
             brief='list all questions', pass_context=True)
async def list_questions(ctx, *args):
    global db
    if len(args) == 0:
        string = db.list_questions()
    else:
        try:
            if len(args) == 1:
                string = db.list_questions(first_index=int(args[0]))
            else:
                string = db.list_questions(first_index=int(args[0]), company=args[1])
        except ValueError:
            string = db.list_questions(company=args[0])

    string = '```' + string + '```'

    await ctx.message.channel.send(content=string)


@bot.command(name='list_companies', description='lists all companies in database', aliases=['lc'],
             brief='list all companies', pass_context=True)
async def list_companies(ctx, *args):
    # all of this can probably be cached until required by waiting for a write or delete to db
    string = "{0:15} | {1:3}\n".format("Company", "Question Count")
    query = db.get_company_list()

    for row in query:
        string += "{0:15} | {1:3}\n".format(row.company, row.count)

    string = '```' + string + '```'
    await ctx.message.channel.send(content=string)


@bot.command(name='remove_question', description='deletes question based on index, found by using >list',
             aliases=['del', 'remove'],
             brief='delete question on index', pass_context=True)
async def remove_question(ctx, *args):
    if not is_mod_or_admin(ctx.message.author, ctx.message.channel):
        await ctx.message.channel.send(content="You have insufficient perms to do this")
        return

    global db, question
    if len(args) == 0:
        await ctx.message.channel.send(content="Please supply index to delete")
        return

    try:
        succ = db.remove_question(int(args[0]))

        if succ is not None:
            if question == succ:
                question = None
            await ctx.message.channel.send( content="Successfully deleted")
        else:
            await ctx.message.channel.send(content="could not find question with supplied index")
    except ValueError:
        await ctx.message.channel.send(content="Please supply **A NUMBER**")


if __name__ == '__main__':
    bot.run(TOKEN)
