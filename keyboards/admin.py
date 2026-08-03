from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Додати товар")],
        [KeyboardButton(text="📦 Додати товар на склад")],
        [KeyboardButton(text="📊 Статистика")]
    ],
    resize_keyboard=True
)