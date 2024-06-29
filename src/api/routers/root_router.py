import datetime

from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

root_router = APIRouter()


@root_router.get('/')
async def root():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({'date': datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")}),
    )
