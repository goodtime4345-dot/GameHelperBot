import asyncio

from payments import get_invoice
from database import (
    get_pending_orders,
    update_order_status,
    get_free_stock,
    use_stock,
)


async def payment_checker(bot):
    while True:
        orders = await get_pending_orders()

        for order in orders:
            order_id = order[0]
            user_id = order[1]
            product_id = order[2]
            invoice_id = order[3]

            invoice = await get_invoice(invoice_id)

            if invoice and invoice.status == "paid":

                stock = await get_free_stock(product_id)

                if stock is None:
                    await bot.send_message(
                        user_id,
                        "❌ Оплату отримано, але товар тимчасово відсутній.\n"
                        "Адміністратор зв'яжеться з вами."
                    )

                    await update_order_status(order_id, "no_stock")
                    continue

                stock_id = stock[0]
                content = stock[1]

                await use_stock(stock_id)
                await update_order_status(order_id, "paid")

                await bot.send_message(
                    user_id,
                    "✅ Оплату успішно отримано!\n\n"
                    "📦 Ваш товар:\n\n"
                    f"<code>{content}</code>"
                )

        await asyncio.sleep(10)