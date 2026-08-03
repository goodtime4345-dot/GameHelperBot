from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

catalog_menu = InlineKeyboardMarkup(
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
                callback_data="metro"
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