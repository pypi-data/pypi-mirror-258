from fastapi_telegrambot.api.v0.api import api_router
from fastapi import FastAPI

application = FastAPI( title = 'fastapi-telegrambot' )
application.include_router( api_router, prefix = '/api' )

__version__ = '0.25'