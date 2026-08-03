from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Каталог")],
        [KeyboardButton(text="📦 Мої замовлення"),
         KeyboardButton(text="👤 Профіль")],
        [KeyboardButton(text="📞 Підтримка")]
    ],
    resize_keyboard=True
)

catalog_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎮 Акаунти")],
        [KeyboardButton(text="🔑 Ключі")],
        [KeyboardButton(text="💎 Донат")],
        [KeyboardButton(text="⭐ Telegram Premium")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)