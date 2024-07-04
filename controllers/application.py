from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

import usecases
from repositories.application import GetOsuFolderPathError

application_router = APIRouter(prefix="/application")

# TODO: create /kill endpoint
# kils osu! process


@application_router.get("/path")
async def get_path():
    try:
        response = usecases.application.get_osu_folder_path()
        return JSONResponse(status_code=200, content=response)
    except GetOsuFolderPathError as e:
        return JSONResponse(status_code=404, content={"error_message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error_message": str(e)})
