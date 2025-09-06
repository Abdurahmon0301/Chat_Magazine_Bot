import asyncio
from aiogram import Dispatcher
from loader import bot
from handlers.catalog import router as catalog_router
from handlers.echo import router as echo_router


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(catalog_router)
    dp.include_router(echo_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


