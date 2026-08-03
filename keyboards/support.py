from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def reply_keyboard(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Відповісти",
                    callback_data=f"reply_{user_id}"
                )
            ]
        ]
    )