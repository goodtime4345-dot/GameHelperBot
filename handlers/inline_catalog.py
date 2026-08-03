from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database import get_products

router = Router()


@router.callback_query(F.data == "catalog")
async def open_catalog(callback: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎮 Акаунти",
                    callback_data="cat_1"
                ),
                InlineKeyboardButton(
                    text="🔑 Ключі",
                    callback_data="cat_2"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚇 Metro",
                    callback_data="cat_5"
                ),
                InlineKeyboardButton(
                    text="💎 Донат",
                    callback_data="cat_3"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⭐ Telegram Premium",
                    callback_data="cat_4"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="home"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        "📂 <b>Каталог</b>\n\nОберіть категорію:",
        reply_markup=keyboard
    )

    await callback.answer()


@router.callback_query(F.data.startswith("cat_"))
async def show_category(callback: CallbackQuery):

    category = int(callback.data.split("_")[1])

    products = await get_products(category)

    if not products:
        await callback.answer(
            "❌ У цій категорії немає товарів.",
            show_alert=True
        )
        return

    keyboard = []

    for product in products:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{product[1]} • {product[3]} USDT",
                    callback_data=f"product_{product[0]}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="catalog"
            )
        ]
    )

    await callback.message.edit_text(
        "🛒 <b>Оберіть товар</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )
    )

    await callback.answer()
from keyboards.inline import buy_keyboard
from database import get_product


@router.callback_query(F.data.startswith("product_"))
async def product(callback: CallbackQuery):

    product_id = int(callback.data.split("_")[1])

    product = await get_product(product_id)

    if not product:
        await callback.answer(
            "❌ Товар не знайдено.",
            show_alert=True
        )
        return

    _, name, description, price, photo, content = product

    caption = (
        f"🛒 <b>{name}</b>\n\n"
        f"{description}\n\n"
        f"💰 <b>{price} USDT</b>"
    )

    await callback.message.delete()

    if photo:
        await callback.message.answer_photo(
            photo,
            caption=caption,
            reply_markup=buy_keyboard(product_id)
        )
    else:
        await callback.message.answer(
            caption,
            reply_markup=buy_keyboard(product_id)
        )

    await callback.answer()    