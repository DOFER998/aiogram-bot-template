from fastapi import FastAPI

from .routers import root_router, webhook_router

app = FastAPI()

app.include_router(root_router)
app.include_router(webhook_router)

__all__ = [
    'app',
]
