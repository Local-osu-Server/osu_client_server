from dataclasses import dataclass
from typing import TypedDict


@dataclass
class ClientPacket:
    ...


class ClientDetails(TypedDict):
    osu_version: float
    osu_path_md5: str
    adapters_md5: str
    uninstall_md5: str
    disk_signature_md5: str
    adapters: list[str]


class LoginInfo(TypedDict):
    username: str
    password_md5: str
    utc_offset: int
    display_city: bool
    pm_private: bool
    client_details: ClientDetails


def login_data(raw_login_data: bytes) -> LoginInfo:
    # username & password
    username, password_md5, client_details = raw_login_data.decode().splitlines()

    # client settings (but osu version is here)
    (
        osu_version,
        utc_offset,
        display_city,
        client_hashes,
        pm_private,
    ) = client_details.split("|")

    # parse client settings

    utc_offset = int(utc_offset)

    if display_city == "0":
        display_city = False
    else:
        display_city = True

    if pm_private == "0":
        pm_private = False
    else:
        pm_private = True

    # parse client details

    osu_version = float(osu_version.removeprefix("b"))

    # split client hashes into individual hashes and remove empty strings
    (osu_path_md5, adapters, adapters_md5, uninstall_md5, disk_signature_md5) = [
        client_hash for client_hash in client_hashes.split(":") if client_hash
    ]

    adapters = adapters.split(".")

    return LoginInfo(
        username=username,
        password_md5=password_md5,
        utc_offset=utc_offset,
        display_city=display_city,
        pm_private=pm_private,
        client_details=ClientDetails(
            osu_version=osu_version,
            osu_path_md5=osu_path_md5,
            adapters_md5=adapters_md5,
            uninstall_md5=uninstall_md5,
            disk_signature_md5=disk_signature_md5,
            adapters=adapters,
        ),
    )
