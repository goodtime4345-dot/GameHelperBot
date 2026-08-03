from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_order_keyboard(order_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Підтвердити",
                    callback_data=f"accept_{order_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Відхилити",
                    callback_data=f"cancel_{order_id}"
                )
            ]
        ]
    )