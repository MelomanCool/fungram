import re

from future.utils import string_types
from telegram import Update, Chat


from . import operators


def all_(update: Update):
    return True


def text(update: Update):
    try:
        return not update.message.text.startswith('/')
    except AttributeError:
        return False


def text_eq(text_):
    def filter_(update: Update):
        try:
            return update.message.text.lower() == text_
        except AttributeError:
            return False

    return filter_


def command(cmd: str):
    cmd = cmd.lower()

    def filter_(update: Update):
        try:
            text_ = update.message.text
            bot_username = update.message.bot.username
        except AttributeError:
            return False

        if not text_:
            return False

        if not (text_.startswith('/') and len(text_) > 1):
            return False

        # skip /, get part before first space, then lowercase
        message_command = text_[1:].split(maxsplit=1)[0].lower()

        return (
                message_command == cmd
                or message_command == cmd + '@' + bot_username.lower()
        )

    return filter_


def regex(pattern):
    def filter_(update: Update):
        try:
            return re.search(pattern, update.message.text, flags=re.IGNORECASE) is not None
        except AttributeError:
            return False

    return filter_


def sticker(update: Update):
    try:
        return bool(update.message.sticker)
    except AttributeError:
        return False


def chat_created(update: Update):
    try:
        return any((
            update.message.group_chat_created,
            update.message.supergroup_chat_created,
            update.message.channel_chat_created
        ))
    except AttributeError:
        return False


def migrate(update: Update):
    try:
        return bool(update.message.migrate_from_chat_id
                    or update.message.migrate_to_chat_id)
    except AttributeError:
        return False


def status_update(update: Update):
    try:
        return any((
            update.message.new_chat_members,
            update.message.left_chat_member,
            update.message.new_chat_title,
            update.message.new_chat_photo,
            update.message.delete_chat_photo,
            update.message.pinned_message,
            chat_created(update),
            migrate(update)
        ))
    except AttributeError:
        return False


def entity(entity_type):
    def filter_(update: Update):
        try:
            return any([entity_.type == entity_type for entity_ in update.message.entities])
        except AttributeError:
            return False

    return filter_


def private(update: Update):
    try:
        return update.message.chat.type == Chat.PRIVATE
    except AttributeError:
        return False


def group(update: Update):
    try:
        return update.message.chat.type in [Chat.GROUP, Chat.SUPERGROUP]
    except AttributeError:
        return False


def user(user_id=None, username=None):
    if not (bool(user_id) ^ bool(username)):
        raise ValueError('One and only one of user_id or username must be used')
    if user_id is not None and isinstance(user_id, int):
        user_ids = [user_id]
    else:
        user_ids = user_id
    if username is None:
        usernames = username
    elif isinstance(username, string_types):
        usernames = [username.replace('@', '')]
    else:
        usernames = [user_.replace('@', '') for user_ in username]

    def filter_(update: Update):
        try:
            user = update.message.from_user
        except AttributeError:
            return False

        if user_ids is not None:
            return bool(user and user.id in user_ids)

        else:
            # self.usernames is not None
            return bool(user and user.username and
                        user.username in usernames)

    return filter_


def chat(chat_id=None, username=None):
    if not (bool(chat_id) ^ bool(username)):
        raise ValueError('One and only one of chat_id or username must be used')
    if chat_id is not None and isinstance(chat_id, int):
        chat_ids = [chat_id]
    else:
        chat_ids = chat_id
    if username is None:
        usernames = username
    elif isinstance(username, string_types):
        usernames = [username.replace('@', '')]
    else:
        usernames = [chat_.replace('@', '') for chat_ in username]

    def filter_(update: Update):
        try:
            chat = update.message.chat
        except AttributeError:
            return False

        if chat_ids is not None:
            return bool(chat.id in chat_ids)
        else:
            # self.usernames is not None
            return bool(chat.username and chat.username in usernames)

    return filter_


def language(lang):
    if isinstance(lang, string_types):
        lang = [lang]
    else:
        lang = lang

    def filter_(update: Update):
        try:
            return update.message.from_user.language_code and any(
                [update.message.from_user.language_code.startswith(x) for x in lang])
        except AttributeError:
            return False

    return filter_


def inline_query(update: Update):
    return bool(update.inline_query)


def chosen_inline_result(update: Update):
    return bool(update.chosen_inline_result)
