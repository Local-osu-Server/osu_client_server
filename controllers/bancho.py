from typing import Literal

from fastapi import Body, Header, Request, Response
from fastapi.routing import APIRouter

import usecases

bancho_router = APIRouter(tags=["Bancho (c* subdomains)"])

# TODO: Handle `CHANGE_ACTION`
# TODO: Handle `SEND_PUBLIC_MESSAGE`
# TODO: Handle `LOGOUT`
# TODO: Handle `REQUEST_STATUS_UPDATE`
# TODO: Handle `PING`
# TODO: Handle `START_SPECTATING`
# TODO: Handle `STOP_SPECTATING`
# TODO: Handle `SPECTATE_FRAMES`
# TODO: Handle `ERROR_REPORT`
# TODO: Handle `CANT_SPECTATE`
# TODO: Handle `SEND_PRIVATE_MESSAGE`
# TODO: Handle `PART_LOBBY`
# TODO: Handle `JOIN_LOBBY`
# TODO: Handle `CREATE_MATCH`
# TODO: Handle `JOIN_MATCH`
# TODO: Handle `PART_MATCH`
# TODO: Handle `MATCH_CHANGE_SLOT`
# TODO: Handle `MATCH_READY`
# TODO: Handle `MATCH_LOCK`
# TODO: Handle `MATCH_CHANGE_SETTINGS`
# TODO: Handle `MATCH_START`
# TODO: Handle `MATCH_SCORE_UPDATE`
# TODO: Handle `MATCH_COMPLETE`
# TODO: Handle `MATCH_CHANGE_MODS`
# TODO: Handle `MATCH_LOAD_COMPLETE`
# TODO: Handle `MATCH_NO_BEATMAP`
# TODO: Handle `MATCH_NOT_READY`
# TODO: Handle `MATCH_FAILED`
# TODO: Handle `MATCH_HAS_BEATMAP`
# TODO: Handle `MATCH_SKIP_REQUEST`
# TODO: Handle `CHANNEL_JOIN`
# TODO: Handle `BEATMAP_INFO_REQUEST`
# TODO: Handle `MATCH_TRANSFER_HOST`
# TODO: Handle `FRIEND_ADD`
# TODO: Handle `FRIEND_REMOVE`
# TODO: Handle `MATCH_CHANGE_TEAM`
# TODO: Handle `CHANNEL_PART`
# TODO: Handle `RECEIVE_UPDATES`
# TODO: Handle `SET_AWAY_MESSAGE`
# TODO: Handle `IRC_ONLY`
# TODO: Handle `USER_STATS_REQUEST`
# TODO: Handle `MATCH_INVITE`
# TODO: Handle `MATCH_CHANGE_PASSWORD`
# TODO: Handle `TOURNAMENT_MATCH_INFO_REQUEST`
# TODO: Handle `USER_PRESENCE_REQUEST`
# TODO: Handle `USER_PRESENCE_REQUEST_ALL`
# TODO: Handle `TOGGLE_BLOCK_NON_FRIEND_DMS`
# TODO: Handle `TOURNAMENT_JOIN_MATCH_CHANNEL`
# TODO: Handle `TOURNAMENT_LEAVE_MATCH_CHANNEL`


@bancho_router.post("/")
async def bancho_handler(
    request: Request,
    osu_token: str | None = Header(None),
    user_agent: Literal["osu!"] = Header(...),
):

    if osu_token is None:  # not logged in, login
        response = await usecases.bancho.login(raw_login_data=await request.body())

        raw_packets = b"".join(
            [packet.to_bancho_protocol() for packet in response["packets"]]
        )

        return Response(
            content=raw_packets, headers={"cho-token": response["osu_token"]}
        )

    # TODO: handle packets
    print("LLOGGED IN")

    print("Osu token:", osu_token)
