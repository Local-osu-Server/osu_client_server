from fastapi.routing import APIRouter
import usecases
from fastapi.responses import JSONResponse

application_router = APIRouter(prefix="/application")

@application_router.get("/path")
async def get_path():
    try:
        response = usecases.application.get_osu_folder_path()
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})