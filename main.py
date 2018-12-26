import os
import peewee

from dotenv import load_dotenv
from os.path import join, dirname
from discord.ext.commands import Bot


# constants
cmd_prefix = '>'
# This is from rolley
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get('TOKEN')

# SQL Database Info
UNAME = os.environ.get('USERNAME')
PWD = os.environ.get('PASSWORD')

bot = Bot(command_prefix=cmd_prefix)
db = peewee.PostgresqlDatabase(
    'daily-bot',
    user=UNAME,
    password=PWD,
    host='localhost'
)


# This is taken mostly from the Peewee sample app
class BaseModel(peewee.Model):
    class Meta:
        database = db


class Question(BaseModel):
    body = peewee.TextField()
    last_date = peewee.DateField()


class Answer(BaseModel):
    uname = peewee.TextField()  # TODO: probably not the best format to save id
    url = peewee.CharField(max_length=2083)
    question = peewee.ForeignKeyField(Question)


def init_db(database=db):
    database.connect()
    database.create_tables([Question, Answer])


if __name__ == '__main__':
    init_db()
