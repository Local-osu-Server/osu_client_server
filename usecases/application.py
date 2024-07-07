from errors import ServerError
from repositories.application import ApplicationRepo


def is_client_running() -> bool:
    """Check if osu! client is running"""

    application_repo = ApplicationRepo()

    return application_repo.is_client_running()


def get_osu_folder_path() -> dict[str, str] | ServerError:
    """Get osu! folder path"""

    application_repo = ApplicationRepo()

    return application_repo.get_osu_folder_path()


def kill_osu() -> dict[str, str] | ServerError:
    """Kill osu! process"""

    application_repo = ApplicationRepo()

    return application_repo.kill_osu()


async def launch_osu() -> dict[str, str] | ServerError:
    """Launch osu!"""

    application_repo = ApplicationRepo()

    return await application_repo.launch_osu()
