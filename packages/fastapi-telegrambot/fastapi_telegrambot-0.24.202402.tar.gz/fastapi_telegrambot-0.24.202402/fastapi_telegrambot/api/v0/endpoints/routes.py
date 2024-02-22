from typing import Optional, NoReturn, List
from fastapi import APIRouter, status
from fastapi_telegrambot.telbot import (
    send_message,
    send_messages,
)

telbotRouter = APIRouter()


@telbotRouter.post( '/send_message', status_code = status.HTTP_200_OK, response_model = None )
async def send_single_message( token: str, chat_id: str, message: str ) -> Optional[ NoReturn ]:

    # TODO: consider handling exception on unknown PEER_ID
    await send_message( token, chat_id, message )
    return


@telbotRouter.post('/send_messages', status_code = status.HTTP_200_OK, response_model = None )
async def send_multiple_messages( messages: List ) -> Optional[ NoReturn ]:

    # TODO: consider handling TG exceptions related to Timeout, TooMuchRequests, etc
    await send_messages( messages )
    return
