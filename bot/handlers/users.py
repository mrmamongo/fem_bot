from collections import Counter
from pathlib import Path
from typing import Callable

import loguru
from aiogram import Router, types, F, Bot
from aiogram.dispatcher.filters.command import CommandStart

from config import settings
from services.recognizer import Recognizer, Gender

user_router = Router()


@user_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет, я бот поддержки в трудную минуту! Скинь свою фотку и я сгенерирую поддержку специально для тебя :)")


@user_router.message(F.content_type.in_({'text', 'photo'}))
async def recognize(bot: Bot, message: types.Message, recognizer: Recognizer, generator: Callable[[Gender], str]):
    filename = Path(settings.recognizer.images_dir) / f"{message.photo[-1].file_id}.jpg"
    loguru.logger.info(f"Saving photo to {filename}")
    await bot.download_file(message.photo[-1].file_id, destination=filename)
    genders = Counter(recognizer.recognize(filename))
    loguru.logger.info(f"Recognized {genders}")
    await message.answer(
        generator(genders.most_common(1)[0][0])
    )
