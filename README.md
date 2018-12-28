[![Build Status](https://travis-ci.org/nikmanG/daily-bot-test.svg?branch=master)](https://travis-ci.org/nikmanG/daily-bot-test)

# Daily-Bot
A bot that outputs coding questions on a daily basis.

## Setup
### Docker
Still doing this

### Normal Script
####Prerequisites:
- Python 3.4.2+
- PostgreSQL
- pip3 (or have pip reference Python 3 installation)

####Installation
Note: this should be pretty generic among all Linux, MacOS, and Windows systems.

- Move into the directory with `main.py`
- Run `pip3 install -r requirements.txt` (or `pip install -r requirements.txt` depending on Python versions)
- Create a `.env` file in the current directory. It should contain the following variables:
```
TOKEN=<Discord Developer Token>
USERNAME=<PostgreSQL account username for bot>
PASSWORD=<PostgreSQL account password for bot>
```
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
Question is in here
```
``````
The bot will reply with what the person should see after minor editing.
Reply **YES** to save the question to the database, **NO** (or anything else) to remove from cache and for you to reformat if needed.
<br>
*NOTE:* Body is unique so if you try add a question that is already in the database, you will be notified that it failed.

### Showing a Question
In the given channel (`daily-coding-challenge` by default), enter `>q` or `>show_question` to get the corresponding question.
This will automatically update on a daily basis.