from typing import TypedDict

from httpx import AsyncClient

BASE_API_URL = "http://localhost:5000/api/v1"

http_client = AsyncClient()


class LoginError(Exception):
    pass


class LoginProfile(TypedDict):
    user_id: int
    username: str


class LoginSession(TypedDict):
    current_osu_token: str
    current_user_id: int
    current_packet_queue: list[dict]  # TODO: typedict the packets


class LoginResponse(TypedDict):
    message: str
    profile: LoginProfile
    session: LoginSession


async def login(username: str) -> LoginResponse:
    response = await http_client.post(
        url=f"{BASE_API_URL}/bancho/login", json={"username": username}
    )

    if response.status_code >= 400:
        # TODO: better error handling for `api.login`
        raise LoginError(f"Failed to login: {response.text}")

    # TODO: typedict the response
    return response.json()


class ProfileResponse(TypedDict):
    user_id: int
    username: str
    accuracy: float
    play_count: int
    total_score: int
    pp: int


async def get_profile(
    user_id: int | None = None,
    username: str | None = None,
) -> ProfileResponse:
    response = await http_client.get(
        url=f"{BASE_API_URL}/profile/",
        params={"user_id": user_id, "username": username},
    )

    if response.status_code >= 400:
        # TODO: better error handling for `api.get_user_stats`
        raise Exception(f"Failed to get user stats: {response.text}")

    return response.json()


class RankFromPPResponse(TypedDict):
    rank: int
    pp: float


async def get_rank(pp: int) -> RankFromPPResponse:
    response = await http_client.get(
        url=f"{BASE_API_URL}/utils/get_rank_from_pp",
        params={"pp": pp},
    )

    if response.status_code >= 400:
        # TODO: better error handling for `api.get_rank`
        raise Exception(f"Failed to get rank: {response.text}")

    return response.json()
