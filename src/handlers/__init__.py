from aiogram import Router


def get_handlers_router() -> Router:
    from .root import get_root_router
    from .user import get_user_router

    router = Router()

    root_router = get_root_router()
    user_router = get_user_router()

    router.include_router(root_router)
    router.include_router(user_router)

    return router
