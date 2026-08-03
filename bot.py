import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database import create_db
from payments import crypto
from payment_checker import payment_checker

from handlers.start import router as start_router
from handlers.inline_catalog import router as inline_catalog_router
from handlers.admin import router as admin_router
from handlers.orders import router as orders_router

dp = Dispatcher()

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)


async def main():
    print("=================================")
    print("✅ Бот успішно запущений")
    print("=================================")

    await create_db()

    dp.include_router(start_router)
    dp.include_router(inline_catalog_router)
    dp.include_router(admin_router)
    dp.include_router(orders_router)

    asyncio.create_task(payment_checker(bot))

    try:
        await dp.start_polling(bot)
    finally:
        await crypto.close()


if __name__ == "__main__":
    asyncio.run(main())