from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database import add_stock, get_all_products
from states import AddStock
from config import ADMIN_ID
from database import add_product
from keyboards.admin import admin_menu
from states import AddProduct
from database import get_statistics

router = Router()


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Доступ заборонено.")
        return

    await message.answer(
        "👑 Адмін-панель",
        reply_markup=admin_menu
    )


@router.message(F.text == "➕ Додати товар")
async def start_add_product(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return

    await state.set_state(AddProduct.category)
    await message.answer(
    "Введіть категорію:\n\n"
    "1 - 🎮 Акаунти\n"
    "2 - 🔑 Ключі\n"
    "3 - 💎 Донат\n"
    "4 - ⭐ Telegram Premium\n"
    "5 - 🚇 Metro"
)

@router.message(AddProduct.category)
async def category(message: Message, state: FSMContext):
    await state.update_data(category=int(message.text))
    await state.set_state(AddProduct.name)
    await message.answer("Введіть назву товару:")


@router.message(AddProduct.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProduct.description)
    await message.answer("Введіть опис товару:")


@router.message(AddProduct.description)
async def description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddProduct.price)
    await message.answer("Введіть ціну (USDT):")


@router.message(AddProduct.price)
async def price(message: Message, state: FSMContext):
    await state.update_data(price=float(message.text))
    await state.set_state(AddProduct.photo)
    await message.answer("📷 Надішліть фото товару.")


@router.message(AddProduct.photo, F.photo)
async def photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id

    await state.update_data(photo=photo_id)
    await state.set_state(AddProduct.content)

    await message.answer(
        "🔑 Надішліть товар, який буде видано після оплати.\n\n"
        "Наприклад:\n"
        "<code>login:password</code>\n"
        "або ключ активації."
    )


@router.message(AddProduct.content)
async def content(message: Message, state: FSMContext):
    data = await state.get_data()

    await add_product(
        data["category"],
        data["name"],
        data["description"],
        data["price"],
        data["photo"],
        message.text
    )

    await state.clear()

    await message.answer(
        "✅ Товар успішно додано!",
        reply_markup=admin_menu
    )

@router.message(F.text == "📦 Додати товар на склад")
async def stock_start(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return

    products = await get_all_products()

    if not products:
        await message.answer("❌ Спочатку створіть хоча б один товар.")
        return

    text = "📦 Список товарів:\n\n"

    for product in products:
        text += f"{product[0]} — {product[1]}\n"

    text += "\nВведіть ID товару:"

    await state.set_state(AddStock.product_id)
    await message.answer(text)


@router.message(AddStock.product_id)
async def stock_product(message: Message, state: FSMContext):
    try:
        product_id = int(message.text)
    except ValueError:
        await message.answer("❌ Введіть числовий ID товару.")
        return

    await state.update_data(product_id=product_id)
    await state.set_state(AddStock.content)

    await message.answer(
        "🔑 Надішліть ключ або акаунт.\n\n"
        "Наприклад:\n"
        "<code>login:password</code>"
    )


@router.message(AddStock.content)
async def stock_content(message: Message, state: FSMContext):
    data = await state.get_data()

    await add_stock(
        data["product_id"],
        message.text
    )

    await state.clear()

    await message.answer(
        "✅ Ключ успішно додано на склад.",
        reply_markup=admin_menu
    )   
@router.message(F.text == "📊 Статистика")
async def statistics(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    users, products, orders, paid, money = await get_statistics()

    await message.answer(
        f"📊 <b>Статистика магазину</b>\n\n"
        f"👥 Користувачів: {users}\n"
        f"🛒 Товарів: {products}\n"
        f"📦 Замовлень: {orders}\n"
        f"✅ Оплачено: {paid}\n"
        f"💰 Дохід: {money} USDT"
    )    