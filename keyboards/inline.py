from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def buy_keyboard(product_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 Купити",
                    callback_data=f"buy_{product_id}"
                )
            ]
        ]
    )