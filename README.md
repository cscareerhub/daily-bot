[![Build Status](https://travis-ci.org/CS-Career-Hackers/daily-bot.svg?branch=master)](https://travis-ci.org/CS-Career-Hackers/daily-bot)
[![Discord Chat](https://img.shields.io/discord/334891772696330241.svg)](https://discord.gg/ndFR4RF)
[![License](https://img.shields.io/github/license/CS-Career-Hackers/daily-bot.svg)](LICENSE)
[![Coverage Status](https://coveralls.io/repos/github/CS-Career-Hackers/daily-bot/badge.svg?branch=master)](https://coveralls.io/github/CS-Career-Hackers/daily-bot?branch=master)
# Daily-Bot
A bot that outputs coding questions on a daily basis.

## Setup
### Docker
#### Prerequisites:
- docker (obviously)
- docker-compose

#### Installation
- Clone this repository into folder of choice.
- Modify [docker-compose.yml](docker-compose.yml) to change the default password and username under `db.environment`.
_I am not being held liable if stuff goes missing because you chose u:`postgres` p:`postgres` for login._
- **NOTE:** If you have PostgreSQL installed on your host you will also have to do the following in [docker-compose.yml](docker-compose.yml):
```
db:
    image: postgres:latest
    restart: always
    ports:
      - '5432:5432'
```
Should have the port changed to read 5431:5432 (or whatever host port isn't taken as Postgres defaults to 5432) as can be seen below:
```
db:
    image: postgres:latest
    restart: always
    ports:
      - '5431:5432'
```

- Create a `.env` file in current directory (look below for how the variables should appear, under Normal Script Installation).
- Run `docker-compose run -d --build` from current directory

### Normal Script
#### Prerequisites:
- Python 3.4.2+
- PostgreSQL
- pip3 (or have pip reference Python 3 installation)

#### Installation
Note: this should be pretty generic among all Linux, MacOS, and Windows systems.

- Run `service postgresql start` to enable the Postgres server. _**Note:** this step may get removed in the future for dockerfile._
- Move into the directory with `main.py`
- Run `pip3 install -r requirements.txt` (or `pip install -r requirements.txt` depending on Python versions)
- Create a `.env` file in the current directory. It should contain the following variables:
```
TOKEN=<Discord Developer Token>
USERNAME=<PostgreSQL account username for bot>
PASSWORD=<PostgreSQL account password for bot>
```
_Note here that you will need to create an account for the postgres user manually, as well as the **dailybot** database._

- Run `python3 main.py` (or again depending on install `python main.py` could suffice).<br>
If successful, this should be present on the terminal:
```
Logged in as
Daily-Bot
00000000000000 # This will vary as it is the Bot ID
------
``` 

## Usage
### Adding a Question
To add a question all you simply have to do is private message the bot the question you want to be added.<br>
It should be inside triple backticks e.g)<br>
``````
```
Company that Asked
Key Data Structure Used
Actual Question
```
``````
The bot will reply with what the person should see after minor editing.
Reply **YES** to save the question to the database, **NO** (or anything else) to remove from cache and for you to reformat if needed.
<br>
*NOTE:* Body is unique so if you try add a question that is already in the database, you will be notified that it failed.

### Showing a Question
In the given channel (`daily-coding-challenge` by default), enter `>q` or `>show_question` to get the corresponding question.
This will automatically update on a daily basis.

If you provide a number index after command e.g `>q 4` it will show the question with the xth index (in this case it will be the 4th).
To find the index of the questions, list through them in ```>lq``` as is explained in Index found by [listing questions](README.md#Listing Questions)..

### Listing Questions
```>lq``` will list the first _10_ questions that were input into the database.
By providing an integer after command, e.g ```>lq 10``` you will get 10 questions starting from provided index.<br>
_NOTE:_ indexing starts at 1, not 0.

### Removing a Question
```>del <index>``` e.g ```>del 10``` deletes a question with given index. Index found by [listing questions](README.md#Listing Questions).
If the question is the day's question, a new one will be found.

## Known Caveats
- When using docker you will need to run `docker-compose up` twice. First time to initialize everything, then `docker-compose down` and `up` again to restart.
Otherwise the Python script will not have access to the backing database.