from pydantic import BaseSettings
from telegram import Bot
from telegram.ext import Application
import os, json

_cpth = os.path.join(
    os.path.dirname( __file__ ),
    'config.json'
)
with open( _cpth, 'r', encoding = 'utf-8' ) as f:

    _conf = json.load( f )


class Settings( BaseSettings ):

    HOST: str = _conf[ 'HOST' ]
    PORT: int = _conf[ 'PORT' ]
    RELOAD: bool = _conf[ 'RELOAD' ]

    PROJECT_NAME: str = _conf[ 'PROJECT_NAME' ]
    FA_API_VERSION: str = _conf[ 'FA_API_VERSION' ]


settings = Settings()


def telbot_instance( tokn: str ) -> Bot:

    return Application.builder().token( tokn ).build().bot
