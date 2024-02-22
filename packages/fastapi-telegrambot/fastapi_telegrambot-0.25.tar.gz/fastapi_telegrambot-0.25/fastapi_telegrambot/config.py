from telegram import Bot
from telegram.ext import Application


def telbot_instance( tokn: str ) -> Bot:

    return Application.builder().token( tokn ).build().bot
