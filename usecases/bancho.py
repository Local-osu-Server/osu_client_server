from typing import TypedDict

import adapters.api as api
import packets.reading as packet_reading
import packets.writing as packet_writing
from packets.writing import ServerPacket


class LoginResponse(TypedDict):
    osu_token: str
    packets: list[ServerPacket]


async def login(raw_login_data: bytes) -> LoginResponse:
    login_info = packet_reading.login_data(raw_login_data)

    try:
        # TODO: utilize logging more 
        login_response = await api.login(username=login_info["username"])

        # we are now logged in server side
        # but we need some more data from the api
        # so we can send the proper login response

        user_stats_response = await api.get_profile(
            user_id=login_response["profile"]["user_id"]
        )

        rank_response = await api.get_rank(pp=user_stats_response["pp"])
    except Exception as e:
        return LoginResponse(
            osu_token="SOMETHING",
            packets=packet_writing.login_error_response(str(e)),
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
