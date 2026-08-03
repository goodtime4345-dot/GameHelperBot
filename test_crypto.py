import asyncio
from payments import create_invoice

async def main():
    invoice = await create_invoice(1, "Test")
    print(invoice)
    print(vars(invoice))

asyncio.run(main())