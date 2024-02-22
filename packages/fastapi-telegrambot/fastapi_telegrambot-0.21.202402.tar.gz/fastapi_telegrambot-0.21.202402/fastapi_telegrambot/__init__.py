from fastapi_telegrambot.api.v0 import api_router
from fastapi_telegrambot.config import settings
from fastapi import FastAPI

application = FastAPI( title = settings.PROJECT_NAME )
application.include_router( api_router, prefix = settings.FA_API_VERSION )

__version__ = '0.21.202402'