#!/usr/bin/env python
"""
    A small bot that uses praw and chatterbot
    Various training types include (manual, reddit, twitter, etc)

    Usage:
        bot.py [-l <level> | --level <level>]
               [-t <type> | --training <type>]

    Options:
        -h --help               Show this screen
        -l --level=<level>      [default: info]
        -t --training=<type>    Training level [default: manual]

    Be sure to export envars first:
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

"""

import os
import sys
import logging
from logging import StreamHandler
from time import sleep
from docopt import docopt
import praw
from chatterbot import ChatBot
from chatterbot.utils import input_function


def logging_setup():
    ''' Setup the logging '''
    argument = docopt(__doc__, version='1.0.0')
    if '--level' in argument and argument.get('--level'):
        level = getattr(logging, argument.get('--level').upper())
    else:
        level = logging.info
    handlers = [StreamHandler()]

    logging.basicConfig(level=level,
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        datefmt="%Y-%m-%d %H:%M:%S",
                        handlers=handlers)

    logger = logging.getLogger('prawcore')

    return logger


def get_gitter_envars():
    """ check if envars are set """

    if os.environ.get('GITTER_ROOM') is None:
        LOG.error("export GITTER_ROOM=''")
        sys.exit(1)
    else:
        gitter_room = os.environ['GITTER_ROOM']

    if os.environ.get('GITTER_API_TOKEN') is None:
        LOG.error("export GITTER_API_TOKEN=''")
        sys.exit(1)
    else:
        gitter_api_token = os.environ['GITTER_API_TOKEN']

    return gitter_room, gitter_api_token


def get_hipchat_envars():
    """ check if envars are set """

    if os.environ.get('HIPCHAT_HOST') is None:
        LOG.error("export HIPCHAT_HOST=''")
        sys.exit(1)
    else:
        hipchat_host = os.environ['HIPCHAT_HOST']

    if os.environ.get('HIPCHAT_ROOM') is None:
        LOG.error("export HIPCHAT_ROOM=''")
        sys.exit(1)
    else:
        hipchat_room = os.environ['HIPCHAT_ROOM']

    if os.environ.get('HIPCHAT_ACCESS_TOKEN') is None:
        LOG.error("export HIPCHAT_ACCESS_TOKEN=''")
        sys.exit(1)
    else:
        hipchat_access_token = os.environ['HIPCHAT_ACCESS_TOKEN']

    return hipchat_host, hipchat_room, hipchat_access_token


def get_twitter_envars():
    """ check if envars are set """

    if os.environ.get('TWITTER_KEY') is None:
        LOG.error("export TWITTER_KEY=''")
        sys.exit(1)
    else:
        twitter_key = os.environ['TWITTER_KEY']

    if os.environ.get('TWITTER_SECRET') is None:
        LOG.error("export TWITTER_SECRET=''")
        sys.exit(1)
    else:
        twitter_secret = os.environ['TWITTER_SECRET']

    if os.environ.get('TWITTER_TOKEN') is None:
        LOG.error("export TWITTER_TOKEN=''")
        sys.exit(1)
    else:
        twitter_token = os.environ['TWITTER_TOKEN']

    if os.environ.get('TWITTER_TOKEN_SECRET') is None:
        LOG.error("export TWITTER_TOKEN_SECRET=''")
        sys.exit(1)
    else:
        twitter_token_secret = os.environ['TWITTER_TOKEN_SECRET']

    return twitter_key, twitter_secret, twitter_token, twitter_token_secret


def get_reddit_envars():
    """ check if envars are set """

    if os.environ.get('REDDIT_CLIENT_ID') is None:
        LOG.error("export REDDIT_CLIENT_ID=''")
        sys.exit(1)
    else:
        client_id = os.environ['REDDIT_CLIENT_ID']

    if os.environ.get('REDDIT_CLIENT_SECRET') is None:
        LOG.error("export REDDIT_CLIENT_SECRET=''")
        sys.exit(1)
    else:
        client_secret = os.environ['REDDIT_CLIENT_SECRET']

    if os.environ.get('REDDIT_USERNAME') is None:
        LOG.error("export REDDIT_USERNAME=''")
        sys.exit(1)
    else:
        username = os.environ['REDDIT_USERNAME']

    if os.environ.get('REDDIT_PASSWORD') is None:
        LOG.error("export REDDIT_PASSWORD=''")
        sys.exit(1)
    else:
        password = os.environ['REDDIT_PASSWORD']

    return client_id, client_secret, username, password


def get_reddit():
    ''' Get praw.Reddit '''

    client_id, client_secret, username, password = get_reddit_envars()
    LOG.debug('%s', client_id)
    LOG.debug('%s', client_secret)
    LOG.debug('%s', username)
    LOG.debug('%s', password)

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent='uselessbots:v0.0.1 (by /u/uselessbots)',
                         username=username,
                         password=password)
    return reddit


def get_sub_comments(comment):
    ''' get sub comments from a reddit comment object as a list '''

    sub_comments = []
    sub_comments.append(comment.body)
    for _idx, child in enumerate(comment.replies):
        sub_comments.append(child.body)

    return sub_comments


def chat_bot():
    ''' https://github.com/gunthercox/ChatterBot '''

    chatbot = ChatBot(
        'Useless Bot',
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database='bot_db',
        database_uri='mongodb://mongo:27017/',
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch'
            },
            # {
            #   'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            #   'threshold': 0.65,
            #   'default_response': 'I am sorry, but I do not understand.'
            # },
            # {
            #   'import_path': 'chatterbot.logic.MathematicalEvaluation'
            # },
            # {
            #   'import_path': 'chatterbot.logic.TimeLogicAdapter'
            # }

        ],

        trainer='chatterbot.trainers.ListTrainer'

        )

    return chatbot


def english_training():
    ''' https://github.com/gunthercox/ChatterBot '''

    from chatterbot.trainers import ChatterBotCorpusTrainer

    LOG.info('Teaching bot basic english...')
    bot = chat_bot()

    bot.set_trainer(ChatterBotCorpusTrainer)
    bot.train("chatterbot.corpus.english")

    return


def ubuntu_training():
    '''
    This is an example showing how to train a chat bot using the
    Ubuntu Corpus of conversation dialog.
    '''

    from chatterbot.trainers import UbuntuCorpusTrainer

    LOG.info('Training bot with ubuntu corpus trainer')
    bot = chat_bot()

    bot.set_trainer(UbuntuCorpusTrainer)
    bot.train()

    return


def reddit_training():
    ''' Grab lim comment trees from r/sub to train the bot '''

    bot = chat_bot()
    reddit = get_reddit()
    # reddit.read_only = True
    LOG.info('Read only?: %s', reddit.read_only)

    lim = 9
    sub = 'all'
    # sub = 'food'
    # sub = 'SubredditSimulator'
    slp = 3

    for submission in reddit.subreddit(sub).hot(limit=lim):

        # easily exceeding rate limits, so we'll sleep
        sleep(slp)

        try:
            LOG.info('Title: %s', submission.title)
            LOG.info('Score: %s', submission.score)
            LOG.info('ID: %s', submission.id)
            LOG.info('URL: %s', submission.url)
            LOG.info('Author: %s', submission.author)
            LOG.info('Link karma: %s', submission.author.link_karma)

            # Comments
            submission.comments.replace_more(limit=0)
            comments_list = submission.comments.list()

            for comment in comments_list:

                sub_comments = get_sub_comments(comment)

                LOG.info('Training: %s', sub_comments)
                bot.train(sub_comments)

            LOG.info('--------------------------------------------------------')

        except praw.exceptions.APIException as praw_exc:
            LOG.error('APIException: %s', praw_exc)

        except praw.exceptions.ClientException as praw_exc:
            LOG.error('ClientException: %s', praw_exc)

        except praw.exceptions.PRAWException as praw_exc:
            LOG.error('PRAWException: %s', praw_exc)

        except AssertionError as exc:
            if '429' in '%s' % exc:
                LOG.warning('Exceeding rate limits: %s', exc)
                LOG.warning('sleeping for 60 seconds')
                sleep(60)


def twitter_training():
    '''
    This example demonstrates how you can train your chat bot
    using data from Twitter.
    '''

    twitter_key, twitter_secret, twitter_token, twitter_token_secret = get_twitter_envars()

    bot = ChatBot(
        'Useless Bot',
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database='bot_db',
        database_uri='mongodb://mongo:27017/',
        logic_adapters=[
            "chatterbot.logic.BestMatch"
        ],
        input_adapter="chatterbot.input.TerminalAdapter",
        output_adapter="chatterbot.output.TerminalAdapter",
        twitter_consumer_key=twitter_key,
        twitter_consumer_secret=twitter_secret,
        twitter_access_token_key=twitter_token,
        twitter_access_token_secret=twitter_token_secret,
        trainer="chatterbot.trainers.TwitterTrainer"
    )

    bot.train()

    bot.logger.info('Trained database generated successfully!')


def manual_training():
    ''' talk to your bot!
        train your bot!
    '''

    bot = chat_bot()
    response = 'How can I help you?'

    while True:

        try:
            training = []
            response = '%s: ' % response
            comment = input(response)
            training.append(str(response))
            training.append(str(comment))
            response = bot.get_response(comment)
            LOG.info('Comment: %s', comment)
            LOG.info('Response: %s', response)
            LOG.info('Training bot: %s', training)
            bot.train(training)

        except (KeyboardInterrupt, EOFError, SystemExit):
            break

    return


def feedback_training():
    """
    This example shows how to create a chat bot that
    will learn responses based on an additional feedback
    element from the user.
    """

    bot = chat_bot()

    CONVERSATION_ID = bot.storage.create_conversation()

    def get_feedback():
        ''' user feedback '''

        text = input_function()

        if 'yes' in text.lower():
            return True
        elif 'no' in text.lower():
            return False
        else:
            print('Please type either "Yes" or "No"')
            return get_feedback()


    print('Type something to begin...')

    # The following loop will execute each time the user enters input
    while True:
        try:
            # input_statement = bot.input.process_input_statement()
            # input_statement = input()
            input_statement = input_function()
            statement, response = bot.generate_response(input_statement, CONVERSATION_ID)
            print('\n Is "{}" this a coherent response to "{}"? \n'.format(response, input_statement))

            if get_feedback():
                bot.learn_response(response, input_statement)
                # Update the conversation history for the bot
                # It is important that this happens last, after the learning step
                bot.storage.add_to_conversation(CONVERSATION_ID, statement, response)

            bot.output.process_response(response)

        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


def hipchat_bot():
    '''
    See the HipChat api documentation for how to get a user access token.
    https://developer.atlassian.com/hipchat/guide/hipchat-rest-api/api-access-tokens
    '''

    hipchat_host, hipchat_room, hipchat_access_token = get_hipchat_envars()
    # bot = chat_bot()

    bot = ChatBot(
        'Useless Bot',
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database='bot_db',
        database_uri='mongodb://mongo:27017/',
        hipchat_host=hipchat_host,
        hipchat_room=hipchat_room,
        hipchat_access_token=hipchat_access_token,
        # input_adapter="chatterbot.input.HipChat",
        input_adapter="chatterbot.input.TerminalAdapter",
        output_adapter='chatterbot.output.HipChat',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

    # bot.train('chatterbot.corpus.english')

    response = 'Hello Human'
    # The following loop will execute each time the user enters input
    while True:
        try:
            response = bot.get_response(None)
            # response = bot.get_response(None)
            # LOG.debug(response)
            # training = []
            # response = '%s: ' % response
            # comment = input(response)
            # training.append(str(response))
            # training.append(str(comment))
            # response = bot.get_response(comment)
            # LOG.info('Comment: %s', comment)
            # LOG.info('Response: %s', response)
            # LOG.info('Training bot: %s', training)
            # bot.train(training)

        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


def gitter_bot():
    ''' gitter bot '''

    gitter_room, gitter_api_token = get_gitter_envars()

    bot = ChatBot(
        'Useless Bot',
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
        database='bot_db',
        database_uri='mongodb://mongo:27017/',
        gitter_room=gitter_room,
        gitter_api_token=gitter_api_token,
        gitter_only_respond_to_mentions=False,
        input_adapter='chatterbot.input.Gitter',
        output_adapter='chatterbot.output.Gitter',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    )

    # bot.train('chatterbot.corpus.english')

    c_id = bot.default_session.uuid
    response = 'Hello Human'
    # The following loop will execute each time the user enters input
    while True:
        try:
            response = bot.get_response(None, c_id)


        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


def main():
    ''' main '''

    argument = docopt(__doc__, version='1.0.0')

    if '--training' in argument and argument.get('--training'):
        training = argument.get('--training')

    if training == 'english':
        english_training()
    elif training == 'manual':
        manual_training()
    elif training == 'feedback':
        feedback_training()
    elif training == 'ubuntu':
        ubuntu_training()
    elif training == 'reddit':
        reddit_training()
    elif training == 'twitter':
        twitter_training()
    elif training == 'hipchat':
        hipchat_bot()
    elif training == 'gitter':
        gitter_bot()
    else:
        LOG.error('Unknown training mode')


if __name__ == '__main__':

    LOG = logging_setup()

    main()
