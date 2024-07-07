import os
from pathlib import Path
from typing import TypedDict

import psutil
from httpx import AsyncClient

from errors import ApplicationRepoError, ServerError


class ConfigJSON(TypedDict):
    osu_folder_path: str
    display_pp_on_leaderboard: bool
    rank_scores_by_pp_or_score: bool
    num_scores_seen_on_leaderboards: int
    allow_pp_from_modified_maps: bool
    osu_api_key: str | None
    osu_daily_api_key: str
    osu_api_v2_client_id: int
    osu_api_v2_client_secret: str
    osu_username: str | None
    osu_password: str | None
    dedicated_dev_server_domain: str


class ApplicationRepo:
    def __init__(self) -> None:
        self.http_client = AsyncClient()

    def is_client_running(self) -> bool:
        """Check if osu! client is running"""

        for process in psutil.process_iter():
            if process.name() == "osu!.exe":
                return True

        return False

    def get_osu_folder_path(self) -> dict[str, str] | ServerError:
        """Get osu! folder path"""

        for process in psutil.process_iter():
            if process.name() == "osu!.exe":
                osu_path = Path(process.cwd())

                return {"message": "osu!.exe found.", "path": str(osu_path)}

        # if the process is not found, return None
        return ServerError(
            error_name=ApplicationRepoError.OSU_NOT_FOUND,
            message="osu!.exe not found.",
            file_location=__file__,
            line=ServerError.get_current_line(),
            status_code=404,
            local_variables=locals(),
            in_scope_variables=dir(),
        )

    def kill_osu(self) -> dict[str, str] | ServerError:
        """Kill osu! process"""

        for process in psutil.process_iter():
            if process.name() == "osu!.exe":
                process.kill()

                return {"message": "osu!.exe killed."}

        return ServerError(
            error_name=ApplicationRepoError.OSU_NOT_FOUND,
            message="osu!.exe not found.",
            file_location=__file__,
            line=ServerError.get_current_line(),
            status_code=404,
            local_variables=locals(),
            in_scope_variables=dir(),
        )

    async def launch_osu(self) -> dict[str, str] | ServerError:
        # TODO: make adaparter for this
        response = await self.http_client.get("http://localhost:5000/api/v1/config/")

        if response.status_code >= 400:
            return ServerError(
                error_name=ApplicationRepoError.CONFIG_API_FAILED,
                message="Error while getting osu! folder path.",
                file_location=__file__,
                line=ServerError.get_current_line(),
                status_code=500,
                local_variables=locals(),
                in_scope_variables=dir(),
            )

        config: ConfigJSON = response.json()

        osu_client = Path(config["osu_folder_path"]) / "osu!.exe"

        print("Dev-server domain:", config["dedicated_dev_server_domain"])

        os.startfile(
            str(osu_client),
            arguments=f"-devserver {config['dedicated_dev_server_domain']}",
        )

        return {"message": "osu! launched."}
