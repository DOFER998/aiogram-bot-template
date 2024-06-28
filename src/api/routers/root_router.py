import datetime

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

root_router = APIRouter()


@root_router.get('/')
async def root():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"),
    )
