from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

import usecases
from errors import ServerError

application_router = APIRouter(prefix="/application", tags=["osu! client"])


@application_router.post("/kill")
async def kill_osu():
    response = usecases.application.kill_osu()
    if isinstance(response, ServerError):
        return JSONResponse(
            status_code=response.status_code,
            content=response.to_dict(),
        )

    return JSONResponse(status_code=200, content=response)


@application_router.get("/path")
async def get_path():
    response = usecases.application.get_osu_folder_path()

    if isinstance(response, ServerError):
        return JSONResponse(
            status_code=response.status_code,
            content=response.to_dict(),
        )

    return JSONResponse(status_code=200, content=response)


@application_router.post("/launch")
async def launch_osu():
    response = await usecases.application.launch_osu()
    if isinstance(response, ServerError):
        return JSONResponse(
            status_code=response.status_code,
            content=response.to_dict(),
        )

    return JSONResponse(status_code=200, content=response)
