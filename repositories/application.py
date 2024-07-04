from pathlib import Path

import psutil


class GetOsuFolderPathError(Exception):
    ...


class ApplicationRepo:
    def __init__(self) -> None:
        pass

    def get_osu_folder_path(self) -> dict[str, str]:
        """Get osu! folder path"""

        for process in psutil.process_iter():
            if process.name() == "osu!.exe":
                osu_path = Path(process.cwd())

                return {"message": "osu!.exe found.", "path": str(osu_path)}

        # if the process is not found, return None
        raise GetOsuFolderPathError("osu!.exe not found.")
