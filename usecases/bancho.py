from typing import TypedDict

import adapters.api as api
import crons.client
import packets.reading as packet_reading
import packets.writing as packet_writing
from errors import ServerError
from packets.writing import ServerPacket


class LoginResponse(TypedDict):
    osu_token: str
    packets: list[ServerPacket]


async def logout(user_id: int) -> None | ServerError:
    response = await api.logout(user_id=user_id)
    return response


async def login(raw_login_data: bytes) -> LoginResponse:
    login_info = packet_reading.login_data(raw_login_data)

    # TODO: utilize logging more
    login_response = await api.login(username=login_info["username"])

    if isinstance(login_response, ServerError):
        login_response.print_error()
        return LoginResponse(
            osu_token="ERROR",
            packets=packet_writing.login_error_response(
                error_message=login_response.detailed_error_message
            ),
        )

    # only set the user id if we are logged in
    # TODO: maybe interrupt the whole idea of a session?
    crons.client.USER_ID = login_response["profile"]["user_id"]

    # we are now logged in server side
    # but we need some more data from the api
    # so we can send the proper login response

    user_stats_response = await api.get_profile(
        user_id=login_response["profile"]["user_id"]
    )

    if isinstance(user_stats_response, ServerError):
        user_stats_response.print_error()
        return LoginResponse(
            osu_token="ERROR",
            packets=packet_writing.login_error_response(
                error_message=user_stats_response.detailed_error_message
            ),
        )

    rank_response = await api.get_rank(pp=user_stats_response["pp"])

    if isinstance(rank_response, ServerError):
        rank_response.print_error()
        return LoginResponse(
            osu_token="ERROR",
            packets=packet_writing.login_error_response(
                error_message=rank_response.detailed_error_message
            ),
        )

    # write the login response packet with all the collected data
    reponse_via_bancho_protocol = packet_writing.login_response(
        user_id=login_response["profile"]["user_id"],
        username=login_response["profile"]["username"],
        accuarcy=user_stats_response["accuracy"],
        play_count=user_stats_response["play_count"],
        total_score=user_stats_response["total_score"],
        rank=rank_response["rank"],
        pp=user_stats_response["pp"],
        utc_offset=login_info["utc_offset"],
        country_code=None,  # TODO: get country code
        longitude=0.0,  # TODO: get longitude (I don't think we need this)
        latitude=0.0,  # TODO: get latitude (I don't think we need this)
    )

    return LoginResponse(
        osu_token=login_response["session"]["current_osu_token"],
        packets=reponse_via_bancho_protocol,
    )
