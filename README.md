[![Build Status](https://travis-ci.org/nikmanG/daily-bot-test.svg?branch=master)](https://travis-ci.org/nikmanG/daily-bot-test)

# Daily-Bot
A bot that outputs coding questions on a daily basis.

## Setup
Haven't gotten this far yet.

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