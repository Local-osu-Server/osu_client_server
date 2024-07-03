from repositories.application import ApplicationRepo


def get_osu_folder_path() -> dict[str, str]:
    """Get osu! folder path"""

    application_repo = ApplicationRepo()

    return application_repo.get_osu_folder_path()
