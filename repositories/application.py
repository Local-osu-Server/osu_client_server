from pathlib import Path

import psutil


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
        return {"message": "No osu!.exe process found."}
