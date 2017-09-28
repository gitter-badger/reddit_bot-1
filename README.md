# Edward
* A small bot that utilizes praw and chatterbot to connect to multiple services
* chatterbot: https://github.com/gunthercox/ChatterBot
* PRAW: https://praw.readthedocs.io/en/latest/

## Dependencies
* python 3.5+
* Be sure to export envars first:
```
export REDDIT_CLIENT_ID=
export REDDIT_CLIENT_SECRET=
export REDDIT_USERNAME=
export REDDIT_PASSWORD=
export TWITTER_KEY=
export TWITTER_SECRET=
export TWITTER_TOKEN=
export TWITTER_TOKEN_SECRET=
export HIPCHAT_HOST=
export HIPCHAT_ROOM=
export HIPCHAT_ACCESS_TOKEN=
export GITTER_ROOM=
export GITTER_API_TOKEN=
```

## TOC
  * [Edward](#edward)
    * [Dependencies](#dependencies)
    * [Usage](#usage)
    * [Docker](#docker)
    * [Module defs](#module-defs)
        * [bot_on_bot()](#bot_on_bot)
        * [bot_sploit()](#bot_sploit)
        * [chat_bot()](#chat_bot)
        * [emoji_preprocessor(bot, statement)](#emoji_preprocessorbot-statement)
        * [english_training()](#english_training)
        * [export(filename=None)](#exportfilenamenone)
        * [feedback_bot()](#feedback_bot)
        * [get_gitter_envars()](#get_gitter_envars)
        * [get_hipchat_envars()](#get_hipchat_envars)
        * [get_reddit()](#get_reddit)
        * [get_reddit_envars()](#get_reddit_envars)
        * [get_sub_comments(comment)](#get_sub_commentscomment)
        * [get_twitter_envars()](#get_twitter_envars)
        * [gitter_bot()](#gitter_bot)
        * [hipchat_bot()](#hipchat_bot)
        * [logging_setup()](#logging_setup)
        * [loop_trainer(input_s)](#loop_trainerinput_s)
        * [main()](#main)
        * [reddit_training(sub, lim)](#reddit_trainingsub-lim)
        * [twitter_training()](#twitter_training)
        * [ubuntu_training()](#ubuntu_training)
        * [voice_bot()](#voice_bot)
        * [word_list_training()](#word_list_training)
## Usage
```
Usage:
    ./edward.py [-l <level> | --level   <level>]
                [-t  <type> | --training <type>]
                [-b   <bot> | --bot       <bot>]
                [-e         | --export   <file>]
                [-h         | --help           ]
                [--version  ]

Options:
    -h --help               Show this screen and exit
    --version               Show version and exit
    -l --level=<level>      [default: info]
    -t --training=<type>    Training type:
                                english, word_list,
                                ubuntu, reddit, twitter
                                [default: None]

    -b --bot=<bot>          Run bot: [default: help]
                                gitter, hipchat, voice, feedback
                                [default: None]
```
## Docker
Build and test with docker-compose
```
make test
```

Build and deploy to docker swarm
```
make deploy

docker stack services edward
ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
i3laoiilqi76        edward_mongo        replicated          1/1                 mongo:latest        *:27017->27017/tcp
qyio6ac50xyt        edward_bot          replicated          1/1                 bot:latest
```
## Module defs
#### `bot_on_bot()`

* make bot talk to another bot.
* https://www.tolearnenglish.com/free/celebs/audreyg.php

#### `bot_sploit()`

* Search for other bots on reddit
* Talk to the other bots on reddit

#### `chat_bot()`

* https://github.com/gunthercox/ChatterBot
* Create default bot
* return chatbot

#### `emoji_preprocessor(bot, statement)`

* input emojis to chatterbot
* http://chatterbot.readthedocs.io/en/stable/preprocessors.html
* http://www.unicode.org/emoji/charts/full-emoji-list.html
* https://github.com/gunthercox/ChatterBot/issues/911

#### `english_training()`

* get base bot [chat_bot()](#chat_bot)
* train basic english with
* [chatterbot.corpus.english](https://github.com/gunthercox/chatterbot-corpus/tree/master/chatterbot_corpus/data/english)

#### `export(filename=None)`

* export the database
* mongoexport -d bot_db -c statements

#### `feedback_bot()`

* ask for input
* present input_statement and response to user
* ask if it makes sense
* if no, user can fix
* train bot

#### `get_gitter_envars()`

* get Gitter room and api token from envars
* you can obtain an api token at:
* https://developer.gitter.im/apps
* return gitter_room, gitter_api_token

#### `get_hipchat_envars()`

* get HipChat host, room, and api token from envars
* you can obtain an api token at:
* https://hipchat.com/admin/api
* return hipchat_host, hipchat_room, hipchat_access_token

#### `get_reddit()`

* obtain client_id, client_secret, username, password from [get_reddit_envars()](#get_reddit_envars)
* set reddit to praw.Reddit
* return reddit

#### `get_reddit_envars()`

* get Reddit creds from envars
* return client_id, client_secret, username, password

#### `get_sub_comments(comment)`

* get sub comments from a reddit comment object as a list
* generate a list of sub_comments from all replies
* return sub_comments

#### `get_twitter_envars()`

* get Twitter creds from envars
* return twitter_key, twitter_secret, twitter_token, twitter_token_secret

#### `gitter_bot()`

* get gitter_room, gitter_api_token from [get_gitter_envars()](#get_gitter_envars)

Talk to bot with twitter or github access
* https://gitter.im/jahrik/edward

#### `hipchat_bot()`

DOES NOT WORK YET

#### `logging_setup()`

* setup logging
* return logger

#### `loop_trainer(input_s)`

- **`input_s`** `str` `required` `default = None`

   Input string

* input string
* process as input_statement
* get statement and response form chat bot
* if the response is not the same as the input string
* train bot with conversation

#### `main()`

* check docopt args

#### `reddit_training(sub, lim)`

- **`sub`** `str` `optional` `default = 'all'`

   Which subreddit to use

- **`lim`** `int` `optional` `default = 9`

   how many to grab

Configure
* get base bot [chat_bot()](#chat_bot)
* get reddit from [get_reddit()](#get_reddit)
* configure read only true/false
* sub = the subreddit to use
* lim = the amount of submissions to grab from a chosen subreddit
* slp = is set to keep from reaching reddit server rate limits

Training
* training list starts as an empty list []
* for every submission collect comment chains
* for every comment in comment chains collect all replies
* if the comment is not '[deleted]'
* if reply is not '[removed]'
* if reply is < 80 characters
* append training list
* Train the bot

#### `twitter_training()`

Train bot using data from Twitter.

#### `ubuntu_training()`

* *THIS IS BROKEN RIGHT NOW*
* get base bot [chat_bot()](#chat_bot)
* train with ubuntu corpus
* [chatterbot.corpus.ubuntu](https://github.com/gunthercox/ChatterBot/blob/b611cbd0629eb2aed9f840b50d1b3f8869c2589e/chatterbot/trainers.py#L236)
* see [Training with the Ubuntu dialog corpus](http://chatterbot.readthedocs.io/en/stable/training.html#training-with-the-ubuntu-dialog-corpus)

#### `voice_bot()`

* input speech to text
* output text to speech

#### `word_list_training()`

* word_list contains 5000 most common words in English language
* randomize the list
* pool 4 child processes
* run [loop_trainer(input_s)](#loop_trainerinput_s) with word as input s 
