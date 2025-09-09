import asyncio
from aiogram import Bot, Dispatcher
from loader import bot
from handlers.catalog import router as catalog_router
from handlers.echo import router as echo_router
from handlers.order import router as order_router
from database import init_db 

API_TOKEN = "8358324570:AAG-z2eluyQcbTzOLNFLTth4QsDEV3RPJRI"

async def main() -> None:

    bot = Bot(token=API_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

 
    init_db() 


    dp.include_router(catalog_router)
    dp.include_router(order_router)
    dp.include_router(echo_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
