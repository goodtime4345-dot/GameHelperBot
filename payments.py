from aiocryptopay import AioCryptoPay, Networks

from config import CRYPTO_PAY_TOKEN

crypto = AioCryptoPay(
    token=CRYPTO_PAY_TOKEN,
    network=Networks.MAIN_NET
)


async def create_invoice(amount: float, description: str):
    invoice = await crypto.create_invoice(
        asset="USDT",
        amount=amount,
        description=description
    )
    return invoice


async def get_invoice(invoice_id: int):
    invoices = await crypto.get_invoices(
        invoice_ids=invoice_id
    )

    if invoices.items:
        return invoices.items[0]

    return None