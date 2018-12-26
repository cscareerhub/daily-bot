import os
import peewee

from dotenv import load_dotenv
from os.path import join, dirname
from discord.ext.commands import Bot
from database import Database


cmd_prefix = '>'

# This is from rolley
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get('TOKEN')
bot = Bot(command_prefix=cmd_prefix)


# SQL Database Info
UNAME = os.environ.get('USERNAME')
PWD = os.environ.get('PASSWORD')

db = Database("daily_bot")
if __name__ == '__main__':
    print("Hello World!")
