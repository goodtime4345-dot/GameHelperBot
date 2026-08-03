from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def payment_keyboard(pay_url: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Оплатити USDT",
                    url=pay_url
                )
            ]
        ]
    )