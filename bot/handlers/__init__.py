from aiogram import Dispatcher
from .users import user_router as users


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(users)
