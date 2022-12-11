from aiogram import Bot, types, Dispatcher
from loguru import logger
from bot.config import settings
from bot.handlers import register_handlers
from bot.middlewares import register_middlewares

bot = Bot(token=settings.telegram.TOKEN, parse_mode="HTML")
dp = Dispatcher()


async def on_startup() -> None:
    logger.info("Starting...")
    register_middlewares(dp)
    # register_filters(dp)
    register_handlers(dp)


async def on_shutdown() -> None:
    logger.warning("Shutting down...")
    await dp.storage.close()
    logger.warning("Exit")


async def main() -> None:
    try:
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(e)
        raise e


def start():
    import asyncio
    asyncio.run(main())


if __name__ == '__main__':
    start()
