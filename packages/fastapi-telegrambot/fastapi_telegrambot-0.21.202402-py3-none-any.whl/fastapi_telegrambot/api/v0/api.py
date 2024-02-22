from fastapi_telegrambot.api.v0.endpoints import routes
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(routes.telbotRouter, tags = ['telegramBot'])