from fastapi_telegrambot.config import telbot_instance
from typing import Optional, NoReturn
import asyncio


async def send_message( token: str, chat_id: str, message: str ) -> Optional[ NoReturn ]:

    tb = telbot_instance( token )
    await tb.send_message( chat_id = chat_id, text = message )


async def send_messages( messages: list ) -> Optional[ NoReturn ]:

    togo = [ telbot_instance( tokn = x[ 0 ] ).send_message( chat_id = x[ 1 ], text = x[ 2 ] ) for x in messages ]
    await asyncio.gather( *togo )
