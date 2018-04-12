from telegram import Bot, Update


def update(*handlers):
    def route(bot: Bot, update: Update):
        for filter_, handler in handlers:
            if filter_(update):
                handler(bot=bot, update=update)
                return True

        else:
            return False

    return route


def conversation_per_user(*handlers):
    user_conv_handler = {}

    def route(bot: Bot, update: Update):
        try:
            user_id = update.message.from_user.id
        except AttributeError:
            return False

        # continue the conversation if user is participating in one
        if user_id in user_conv_handler.keys():
            try:
                user_conv_handler[user_id].send((bot, update))
            except StopIteration:
                user_conv_handler.pop(user_id)
            return True

        for filter_, handler_generator in handlers:
            if filter_(update):
                handler = handler_generator()
                next(handler)
                try:
                    handler.send((bot, update))
                    user_conv_handler[user_id] = handler
                except StopIteration:
                    pass
                return True

        return False

    return route
