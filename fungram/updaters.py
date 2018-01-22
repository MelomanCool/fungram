from time import sleep

from telegram import Bot
from telegram.error import TimedOut


def long_polling(token, routers, timeout=10):
    """Polls Telegram server for updates"""
    bot = Bot(token)
    last_update_id = None

    while True:
        try:
            updates = bot.get_updates(offset=last_update_id, timeout=timeout)
            if updates:
                last_update_id = updates[-1].update_id + 1

            for update in updates:
                for route in routers:
                    if route(bot, update):
                        break

            sleep(1)

        except TimedOut:
            continue

        except KeyboardInterrupt:
            break
