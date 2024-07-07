import asyncio

import usecases
from common.log import LogTypes, log

USER_ID: int | None = None


async def check_if_client_is_closed() -> None:
    global USER_ID
    while True:
        if usecases.application.is_client_running():
            # log("Client is running, waiting 2 seconds", LogTypes.INFO)
            await asyncio.sleep(2)
            continue

        if USER_ID is None:
            # log("Client is closed, but no user is logged in", LogTypes.INFO)
            await asyncio.sleep(2)
            continue

        # if it is not running, we gotta log the user out and close the session

        log("Client is closed, logging out user", LogTypes.INFO)

        await usecases.bancho.logout(USER_ID)

        log("User logged out, resetting user id", LogTypes.SUCCESS)

        USER_ID = None
