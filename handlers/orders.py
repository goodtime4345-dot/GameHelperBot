from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import ADMIN_ID
from database import (
    create_order,
    get_product,
    update_order_status,
)
from payments import create_invoice
from keyboards.orders import admin_order_keyboard
from keyboards.payment import payment_keyboard

router = Router()


@router.callback_query(F.data.startswith("buy_"))
async def buy_product(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])

    product = await get_product(product_id)

    if not product:
        await callback.answer("❌ Товар не знайдено", show_alert=True)
        return

    # Створюємо інвойс Crypto Pay
    invoice = await create_invoice(
        amount=float(product[3]),
        description=product[1]
    )

    # Зберігаємо замовлення разом з invoice_id
    order_id = await create_order(
        callback.from_user.id,
        product_id,
        invoice.invoice_id
    )

    await callback.message.answer(
        f"💳 Замовлення №{order_id}\n\n"
        f"🛒 {product[1]}\n"
        f"💰 {product[3]} USDT\n\n"
        f"Натисніть кнопку нижче для оплати.",
        reply_markup=payment_keyboard(invoice.bot_invoice_url)
    )

    await callback.bot.send_message(
        ADMIN_ID,
        f"📦 Нове замовлення №{order_id}\n\n"
        f"👤 {callback.from_user.full_name}\n"
        f"🆔 {callback.from_user.id}\n"
        f"🛒 {product[1]}\n"
        f"💰 {product[3]} USDT",
        reply_markup=admin_order_keyboard(order_id)
    )

    await callback.answer()


@router.callback_query(F.data.startswith("accept_"))
async def accept_order(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[1])

    await update_order_status(order_id, "accepted")

    await callback.message.edit_text(
        callback.message.text + "\n\n✅ Замовлення підтверджено"
    )

    await callback.answer("Підтверджено")


@router.callback_query(F.data.startswith("cancel_"))
async def cancel_order(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[1])

    await update_order_status(order_id, "cancelled")

    await callback.message.edit_text(
        callback.message.text + "\n\n❌ Замовлення відхилено"
    )

    await callback.answer("Скасовано")