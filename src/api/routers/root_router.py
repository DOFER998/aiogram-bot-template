from datetime import datetime

from fastapi import APIRouter

root_router = APIRouter()


@root_router.get('/')
async def root():
    return {
        'status': 200,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
