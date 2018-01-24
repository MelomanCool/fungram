"""Helper decorators.

These decorators give you the ability to describe how you want to get
the updates. Do you want to receive message instead of update? Or do
you want to get parsed arguments? These helpers are for you!"""

from telegram import Update


def message(handler):
    def inner(update: Update, *args, **kwargs):
        return handler(update=update, message=update.message, *args, **kwargs)

    return inner


def command_arguments_raw(handler):
    def inner(update: Update, *args, **kwargs):
        if ' ' not in update.message.text:
            arguments = ''

        else:
            arguments = update.message.text.split(maxsplit=1)[1]
        return handler(update=update, arguments=arguments, *args, **kwargs)

    return inner


def command_arguments_parsed(handler):
    def inner(update: Update, *args, **kwargs):
        if ' ' not in update.message.text:
            arguments = []

        else:
            arguments = update.message.text.split()[1:]

        return handler(update=update, arguments=arguments, *args, **kwargs)

    return inner
