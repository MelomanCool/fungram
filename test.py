from telegram import Message

import config
from fungram import extract
from fungram import filters
from fungram import routers
from fungram.routers import FilterHandler
from fungram.updaters import long_polling


@extract.message
def ping(message: Message, **kwargs):
    message.reply_text('Pong')


@extract.message
def echo(message: Message, **kwargs):
    message.reply_text(message.text)


@extract.message
@extract.command_arguments_raw
def test(message: Message, arguments: str, **kwargs):
    if not arguments:
        arguments = 'No arguments'
    message.reply_text(arguments)


def conversation_handler():
    state = 'start'

    while True:
        _, update = yield

        if filters.command('cancel')(update):
            update.message.reply_text('Okay, ending the conversation.')
            break

        if state == 'start':
            update.message.reply_text('Hello!')
            state = 'already_know'

        elif state == 'already_know':
            update.message.reply_text('I already know you!')
            state = 'boring'

        elif state == 'boring':
            update.message.reply_text('Yeah, boring...')
            break


def main():
    long_polling(config.TOKEN, routers=[
        routers.conversation_per_user(
            FilterHandler(filters.text_eq('hello'), conversation_handler),
        ),
        routers.update(
            FilterHandler(filters.command('test'), test),
            FilterHandler(filters.text_eq('ping'), ping),
            FilterHandler(filters.text,            echo),
        )
    ])


if __name__ == '__main__':
    main()
