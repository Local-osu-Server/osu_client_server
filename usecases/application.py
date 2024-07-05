from repositories.application import ApplicationRepo


def get_osu_folder_path() -> dict[str, str]:
    """Get osu! folder path"""

    application_repo = ApplicationRepo()

    return application_repo.get_osu_folder_path()


def kill_osu() -> dict[str, str]:
    """Kill osu! process"""

    application_repo = ApplicationRepo()

    return application_repo.kill_osu()


async def launch_osu() -> dict[str, str]:
    """Launch osu!"""

    application_repo = ApplicationRepo()

    return await application_repo.launch_osu()
