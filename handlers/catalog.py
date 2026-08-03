from aiogram import Router, F
from aiogram.types import Message

from keyboards.inline import buy_keyboard
from database import get_products
from keyboards.menu import catalog_menu, main_menu

router = Router()


@router.message(F.text == "🛍 Каталог")
async def open_catalog(message: Message):
    await message.answer(
        "🛍 Оберіть категорію:",
        reply_markup=catalog_menu
    )


async def show_products(message: Message, category: int):
    products = await get_products(category)

    if not products:
        await message.answer("❌ У цій категорії немає товарів.")
        return

    for product in products:
        product_id = product[0]
        name = product[1]
        description = product[2]
        price = product[3]
        photo = product[4]

        caption = (
            f"🛒 <b>{name}</b>\n\n"
            f"{description}\n\n"
            f"💰 Ціна: <b>{price} грн</b>"
        )

        if photo:
            await message.answer_photo(
                photo=photo,
                caption=caption,
                reply_markup=buy_keyboard(product_id)
            )
        else:
            await message.answer(
                caption,
                reply_markup=buy_keyboard(product_id)
            )


@router.message(F.text == "🎮 Акаунти")
async def accounts(message: Message):
    await show_products(message, 1)


@router.message(F.text == "🔑 Ключі")
async def keys(message: Message):
    await show_products(message, 2)


@router.message(F.text == "💎 Донат")
async def donate(message: Message):
    await show_products(message, 3)


@router.message(F.text == "⭐ Telegram Premium")
async def premium(message: Message):
    await show_products(message, 4)


@router.message(F.text == "⬅️ Назад")
async def back(message: Message):
    await message.answer(
        "🏠 Головне меню",
        reply_markup=main_menu
    )