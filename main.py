from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.log import setup_logging
from controllers.application import application_router
from controllers.bancho import bancho_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.logger = setup_logging()

    app.include_router(application_router)

    for prefix in ("c", "ce", "c4", "c5", "c6"):
        app.include_router(bancho_router, prefix=f"/{prefix}")

    # TODO: Handle /assets/*
    # TODO: Handle /web/*
    # TODO: Handle /a/*
    # TODO: Handle /b/*
    # TODO: Handle /osu/*

    yield


app = FastAPI(lifespan=lifespan)

# TODO: understand this solution, https://github.com/tiangolo/fastapi/issues/1663
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", port=5001, reload=True)
