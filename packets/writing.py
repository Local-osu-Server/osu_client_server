import struct
from enum import IntEnum
from typing import Any

from common.game_mode import GameMode


class ServerPacketIDS(IntEnum):
    USER_ID = 5
    SEND_MESSAGE = 7
    PONG = 8
    HANDLE_IRC_CHANGE_USERNAME = 9
    HANDLE_IRC_QUIT = 10
    USER_STATS = 11
    USER_LOGOUT = 12
    SPECTATOR_JOINED = 13
    SPECTATOR_LEFT = 14
    SPECTATE_FRAMES = 15
    VERSION_UPDATE = 19
    SPECTATOR_CANT_SPECTATE = 22
    GET_ATTENTION = 23
    NOTIFICATION = 24
    UPDATE_MATCH = 26
    NEW_MATCH = 27
    DISPOSE_MATCH = 28
    TOGGLE_BLOCK_NON_FRIEND_DMS = 34
    MATCH_JOIN_SUCCESS = 36
    MATCH_JOIN_FAIL = 37
    FELLOW_SPECTATOR_JOINED = 42
    FELLOW_SPECTATOR_LEFT = 43
    ALL_PLAYERS_LOADED = 45
    MATCH_START = 46
    MATCH_SCORE_UPDATE = 48
    MATCH_TRANSFER_HOST = 50
    MATCH_ALL_PLAYERS_LOADED = 53
    MATCH_PLAYER_FAILED = 57
    MATCH_COMPLETE = 58
    MATCH_SKIP = 61
    UNAUTHORIZED = 62  # unused
    CHANNEL_JOIN_SUCCESS = 64
    CHANNEL_INFO = 65
    CHANNEL_KICK = 66
    CHANNEL_AUTO_JOIN = 67
    BEATMAP_INFO_REPLY = 69
    PRIVILEGES = 71
    FRIENDS_LIST = 72
    PROTOCOL_VERSION = 75
    MAIN_MENU_ICON = 76
    MONITOR = 80  # unused
    MATCH_PLAYER_SKIPPED = 81
    USER_PRESENCE = 83
    RESTART = 86
    MATCH_INVITE = 88
    CHANNEL_INFO_END = 89
    MATCH_CHANGE_PASSWORD = 91
    SILENCE_END = 92
    USER_SILENCED = 94
    USER_PRESENCE_SINGLE = 95
    USER_PRESENCE_BUNDLE = 96
    USER_DM_BLOCKED = 100
    TARGET_IS_SILENCED = 101
    VERSION_UPDATE_FORCED = 102
    SWITCH_SERVER = 103
    ACCOUNT_RESTRICTED = 104
    RTX = 105  # unused
    MATCH_ABORT = 106
    SWITCH_TOURNAMENT_SERVER = 107


class ClientPacketIDS(IntEnum):
    ...


class Action(IntEnum):
    # The client's current status
    Idle = 0
    Afk = 1
    Playing = 2
    Editing = 3
    Modding = 4
    Multiplayer = 5
    Watching = 6
    Unknown = 7
    Testing = 8
    Submitting = 9
    Paused = 10
    Lobby = 11
    Multiplaying = 12
    OsuDirect = 13


class UnsignedInt(int):
    ...


class Short(int):
    ...


class Listi32(list[int]):
    ...


class OsuByte(int):
    ...


class OsuUnsignedByte(int):
    ...


class LongLongInt(int):
    ...


class ServerPacket:
    def __init__(
        self,
        packet_id: ServerPacketIDS,
        packet_data: dict[str, Any] = {},
    ) -> None:
        self.packet_id: ServerPacketIDS = packet_id
        self.packet_data: dict[str, Any] = packet_data

    def write_uleb128(self, num: int) -> bytes:
        if num == 0:
            return bytearray(b"\x00")

        ret = bytearray()
        length = 0

        while num > 0:
            ret.append(num & 0b01111111)
            num >>= 7
            if num != 0:
                ret[length] |= 0b10000000
            length += 1

        return bytes(ret)

    def write_unsigned_int(self, i: int) -> bytes:
        return struct.pack("<I", i)

    def write_int(self, i: int) -> bytes:
        return struct.pack("<i", i)

    def write_string(self, string: str) -> bytes:
        s = string.encode()
        return b"\x0b" + self.write_uleb128(len(s)) + s

    def write_short(self, value: int) -> bytes:
        return struct.pack("<h", value)

    def write_list32(self, list_of_ints: Listi32) -> bytes:
        # write list length
        ret = bytearray(self.write_short(len(list_of_ints)))

        # write list items
        for item in list_of_ints:
            ret += self.write_int(item)

        return bytes(ret)

    def write_byte(self, value: OsuByte) -> bytes:
        return struct.pack("<b", value)

    def write_long_long(self, value: LongLongInt) -> bytes:
        return struct.pack("<q", value)

    def write_unsigned_byte(self, value: OsuUnsignedByte) -> bytes:
        return struct.pack("<B", value)

    def write_float(self, value: float) -> bytes:
        return struct.pack("<f", value)

    def to_bancho_protocol(self) -> bytes:
        # write packet id & compression bool
        packet = bytearray(struct.pack("<Hx", self.packet_id))

        for key, value in self.packet_data.items():
            # check custom types first
            if isinstance(value, UnsignedInt):
                packet += self.write_unsigned_int(value)
            elif isinstance(value, Listi32):
                packet += self.write_list32(value)
            elif isinstance(value, Short):
                packet += self.write_short(value)
            elif isinstance(value, OsuByte):
                packet += self.write_byte(value)
            elif isinstance(value, LongLongInt):
                packet += self.write_long_long(value)
            elif isinstance(value, OsuUnsignedByte):
                packet += self.write_unsigned_byte(value)

            # check built-in types
            elif isinstance(value, str):
                packet += self.write_string(value)
            elif isinstance(value, int):
                packet += self.write_int(value)
            elif isinstance(value, float):
                packet += self.write_float(value)
            else:
                raise ValueError(f"Invalid type {type(value)} for value {key}: {value}")

        # write data length
        packet[3:3] = struct.pack("<I", len(packet) - 3)

        return bytes(packet)


class UserIDPacket(ServerPacket):
    def __init__(
        self,
        user_id: int,
    ) -> None:

        if user_id > 0:
            user_id = UnsignedInt(user_id)

        super().__init__(
            packet_id=ServerPacketIDS.USER_ID, packet_data={"user_id": user_id}
        )


class NotificationPacket(ServerPacket):
    def __init__(
        self,
        message: str,
    ) -> None:

        super().__init__(
            packet_id=ServerPacketIDS.NOTIFICATION, packet_data={"message": message}
        )


class ProtocolVersionPacket(ServerPacket):
    def __init__(
        self,
    ) -> None:

        super().__init__(
            packet_id=ServerPacketIDS.PROTOCOL_VERSION, packet_data={"version": 19}
        )


class FriendsListPacket(ServerPacket):
    def __init__(
        self,
        friends: list[int],
    ) -> None:
        """friends: list of user ids"""

        # TODO: Understand wether we need to send the whole user's friends list or just the online ones

        friends = Listi32(friends)

        super().__init__(
            packet_id=ServerPacketIDS.FRIENDS_LIST, packet_data={"friends": friends}
        )


class MainMenuIconPacket(ServerPacket):
    def __init__(
        self,
        image: str,
        click_link: str,
    ) -> None:

        image_and_click_link = "|".join([image, click_link])

        super().__init__(
            packet_id=ServerPacketIDS.MAIN_MENU_ICON,
            packet_data={"image_and_click_link": image_and_click_link},
        )


class ChannelInfoPacket(ServerPacket):
    def __init__(
        self,
        channel_name: str,
        channel_description: str,
    ) -> None:

        if not channel_name.startswith("#"):
            channel_name = f"#{channel_name}"

        super().__init__(
            packet_id=ServerPacketIDS.CHANNEL_INFO,
            packet_data={
                "channel_name": channel_name,
                "channel_description": channel_description,
                "channel_player_count": Short(1),
            },
        )


class BanchoPrivilegesPacket(ServerPacket):
    def __init__(
        self,
        privileges: int,
    ) -> None:

        super().__init__(
            packet_id=ServerPacketIDS.PRIVILEGES, packet_data={"privileges": privileges}
        )


class ChannelInfoEndPacket(ServerPacket):
    def __init__(
        self,
    ) -> None:

        super().__init__(packet_id=ServerPacketIDS.CHANNEL_INFO_END)


class ChannelJoinPacket(ServerPacket):
    def __init__(
        self,
        channel_name: str,
    ) -> None:

        if not channel_name.startswith("#"):
            channel_name = f"#{channel_name}"

        super().__init__(
            packet_id=ServerPacketIDS.CHANNEL_JOIN_SUCCESS,
            packet_data={"channel_name": channel_name},
        )


class UserStatsPacket(ServerPacket):
    def __init__(
        self,
        user_id: int,
        action: Action,  # model
        info_text: str,  # TODO: what is info_text?
        current_map_md5: str,
        current_mods_enabled: int,
        game_mode: GameMode,
        current_map_id: int,  # probably the beatmap id
        ranked_score: int,
        accuracy: float,
        play_count: int,
        total_score: int,
        rank: int,
        pp: int,
    ) -> None:

        # TODO: is the type checker correct?
        action = OsuByte(action.value)  # type: ignore
        game_mode = OsuUnsignedByte(game_mode.value)  # type: ignore

        ranked_score = LongLongInt(ranked_score)
        total_score = LongLongInt(total_score)
        pp = Short(pp)

        accuracy = accuracy / 100.0

        super().__init__(
            packet_id=ServerPacketIDS.USER_STATS,
            packet_data={
                "user_id": user_id,
                "action": action,
                "info_text": info_text,
                "map_md5": current_map_md5,
                "mods": current_mods_enabled,
                "mode": game_mode,
                "map_id": current_map_id,
                "ranked_score": ranked_score,
                "accuracy": accuracy,
                "playcount": play_count,
                "total_score": total_score,
                "rank": rank,
                "pp": pp,
            },
        )


class UserPresencePacket(ServerPacket):
    def __init__(
        self,
        user_id: int,
        username: str,
        utc_offset: int,
        country_code: int,
        bancho_privliges: int,
        game_mode: GameMode,
        longitude: float,
        latitude: float,
        rank: int,
    ) -> None:

        bancho_privliges_and_game_mode = OsuUnsignedByte(
            bancho_privliges | game_mode.value << 5
        )
        utc_offset = OsuUnsignedByte(utc_offset + 24)
        country_code = OsuUnsignedByte(country_code)

        super().__init__(
            packet_id=ServerPacketIDS.USER_PRESENCE_SINGLE,
            packet_data={
                "user_id": user_id,
                "username": username,
                "utc_offset": utc_offset,
                "country_code": country_code,
                "bancho_privliges_and_game_mode": bancho_privliges_and_game_mode,
                "longitude": longitude,
                "latitude": latitude,
                "rank": rank,
            },
        )


def login_error_response(error_message: str) -> list[ServerPacket]:
    return [
        UserIDPacket(user_id=-1),  # -1 is an error code
        NotificationPacket(message=error_message),
    ]


def login_response(
    user_id: int,
    username: str,
    accuarcy: float,  # TODO: get the user's accuracy
    play_count: int,  # TODO: get the user's play count
    total_score: int,  # TODO: get the user's total score
    rank: int,  # TODO: get the user's rank
    pp: int,  # TODO: get the user's pp
    utc_offset: int | None = None,  # TODO: get the user's utc offset
    country_code: int | None = None,  # TODO: get the user's country code
    longitude: float = 0.0,  # TODO: get the user's longitude
    latitude: float = 0.0,  # TODO: get the user's latitude
) -> list[ServerPacket]:
    # userid
    # notification
    # protocol_version
    # bancho privileges
    # friends list
    # main menu icon
    # channels
    # user stats
    # user presence

    user_id_packet = UserIDPacket(user_id=user_id)

    notifcation_packet = NotificationPacket(
        message="Succesfully Logged into Local osu! Server!"
    )

    protocol_version_packet = ProtocolVersionPacket()

    bancho_privileges_packet = BanchoPrivilegesPacket(
        privileges=63  # Constant, all privileges to the user
    )

    friends_list_packet = FriendsListPacket(friends=[])

    main_menu_icon_packet = MainMenuIconPacket(
        image="https://avatars.githubusercontent.com/u/174163885?s=200&v=4",
        click_link="https://github.com/Local-osu-Server",
    )

    # TODO: Store Channel Info in the database
    # For now we can just send the default channels

    osu_channel_packet = ChannelInfoPacket(
        channel_name="osu",
        channel_description="x",
    )

    recent_scores_channel_packet = ChannelInfoPacket(
        channel_name="recent_scores",
        channel_description="Shows recently submitted scores",
    )

    recent_top_scores_channel_packet = ChannelInfoPacket(
        channel_name="recent_top_scores",
        channel_description="Shows recently submitted top scores",
    )

    channel_info_end_packet = ChannelInfoEndPacket()

    joined_osu_channel_packet = ChannelJoinPacket(channel_name="osu")

    joined_recent_scores_channel_packet = ChannelJoinPacket(
        channel_name="recent_scores"
    )

    joined_recent_top_scores_channel_packet = ChannelJoinPacket(
        channel_name="recent_top_scores"
    )

    user_stats_packet = UserStatsPacket(
        user_id=user_id,
        action=Action.Idle,  # Constant
        info_text="",  # Constant
        current_map_md5="",  # Constant
        current_mods_enabled=0,  # Constant
        game_mode=GameMode.STANDARD,  # Constant
        current_map_id=0,  # Constant
        ranked_score=0,  # Constant
        accuracy=accuarcy,
        play_count=play_count,
        total_score=total_score,
        rank=rank,
        pp=pp,
    )

    user_precense_packet = UserPresencePacket(
        user_id=user_id,
        username=username,
        utc_offset=utc_offset if utc_offset else 0,
        country_code=country_code if country_code else 0,
        bancho_privliges=63,  # Constant
        game_mode=GameMode.STANDARD,  # Constant
        longitude=longitude if longitude else 0.0,
        latitude=latitude if latitude else 0.0,
        rank=rank,
    )

    return [
        user_id_packet,
        notifcation_packet,
        protocol_version_packet,
        bancho_privileges_packet,
        friends_list_packet,
        main_menu_icon_packet,
        osu_channel_packet,
        recent_scores_channel_packet,
        recent_top_scores_channel_packet,
        channel_info_end_packet,
        joined_osu_channel_packet,
        joined_recent_scores_channel_packet,
        joined_recent_top_scores_channel_packet,
        user_stats_packet,
        user_precense_packet,
    ]
