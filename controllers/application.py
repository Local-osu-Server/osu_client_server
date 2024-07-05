from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

import usecases
from repositories.application import GetOsuFolderPathError

application_router = APIRouter(prefix="/application")

# TODO: create /kill endpoint
# kils osu! process


@application_router.post("/kill")
async def kill_osu():
    try:
        response = usecases.application.kill_osu()
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error_message": str(e)})


@application_router.get("/path")
async def get_path():
    try:
        response = usecases.application.get_osu_folder_path()
        return JSONResponse(status_code=200, content=response)
    except GetOsuFolderPathError as e:
        return JSONResponse(status_code=404, content={"error_message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error_message": str(e)})


@application_router.post("/launch")
async def launch_osu():
    try:
        response = await usecases.application.launch_osu()
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error_message": str(e)})
