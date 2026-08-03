from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📂 Каталог",
                callback_data="catalog"
            )
        ],
        [
            InlineKeyboardButton(
                text="📦 Мої замовлення",
                callback_data="orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="👤 Профіль",
                callback_data="profile"
            ),
            InlineKeyboardButton(
                text="📞 Підтримка",
                callback_data="support"
            )
        ]
    ]
)