from aiogram import Dispatcher

from bot.middlewares.generator import GeneratorMiddleware
from bot.middlewares.recognizer import RecognizerMiddleware


def register_middlewares(dp: Dispatcher) -> None:
    dp.message.middleware.register(GeneratorMiddleware())
    dp.message.middleware.register(RecognizerMiddleware())
