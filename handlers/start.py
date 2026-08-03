from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from keyboards.catalog import catalog_menu

from config import ADMIN_ID
from keyboards.main import main_menu
from keyboards.support import reply_keyboard
from database import get_user_orders
from states import Support, ReplySupport

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "👋 <b>Ласкаво просимо до Samurai Shop!</b>\n\n"
        "Оберіть потрібний розділ:",
        reply_markup=main_menu
    )


@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):

    username = (
        f"@{callback.from_user.username}"
        if callback.from_user.username
        else "немає"
    )

    await callback.message.edit_text(
        f"👤 <b>Профіль</b>\n\n"
        f"🆔 ID: <code>{callback.from_user.id}</code>\n"
        f"👤 Ім'я: {callback.from_user.full_name}\n"
        f"📛 Username: {username}",
        reply_markup=main_menu
    )

    await callback.answer()


@router.callback_query(F.data == "support")
async def support(callback: CallbackQuery, state: FSMContext):

    await state.set_state(Support.message)

    await callback.message.edit_text(
    "💬 <b>Підтримка</b>\n\n"
    "Напишіть своє повідомлення.\n"
    "Воно буде автоматично надіслано адміністратору.",
    reply_markup=main_menu
)

    await callback.answer()


@router.message(Support.message)
async def support_send(message: Message, state: FSMContext):
    username = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else "немає"
    )

    await message.bot.send_message(
        ADMIN_ID,
        f"📩 <b>Нове звернення</b>\n\n"
        f"👤 {message.from_user.full_name}\n"
        f"🆔 {message.from_user.id}\n"
        f"📛 {username}\n\n"
        f"💬 {message.text}",
        reply_markup=reply_keyboard(message.from_user.id)
    )

    await state.clear()

    await message.answer(
    "✅ Ваше повідомлення успішно відправлено.\n"
    "Адміністратор відповість найближчим часом.",
    reply_markup=main_menu
 )


@router.callback_query(F.data.startswith("reply_"))
async def reply_start(callback: CallbackQuery, state: FSMContext):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer()
        return

    user_id = int(callback.data.split("_")[1])

    await state.update_data(user_id=user_id)
    await state.set_state(ReplySupport.message)

    await callback.message.answer(
        "✍️ Введіть відповідь користувачу:"
    )

    await callback.answer()


@router.message(ReplySupport.message)
async def reply_send(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    data = await state.get_data()

    await message.bot.send_message(
        data["user_id"],
        f"💬 <b>Відповідь підтримки</b>\n\n"
        f"{message.text}"
    )

    await state.clear()

    await message.answer(
    "✅ Відповідь успішно відправлена.",
    reply_markup=main_menu
)




@router.callback_query(F.data == "orders")
async def my_orders(callback: CallbackQuery):

    orders = await get_user_orders(callback.from_user.id)

    if not orders:
        await callback.message.edit_text(
            "📦 У вас поки що немає замовлень.",
            reply_markup=main_menu
        )
        await callback.answer()
        return

    text = "📦 <b>Мої замовлення</b>\n\n"

    for name, price, status, date in orders:

        if status == "paid":
            status_text = "✅ Оплачено"
        elif status == "pending":
            status_text = "⏳ Очікує оплату"
        elif status == "accepted":
            status_text = "✅ Видано"
        elif status == "cancelled":
            status_text = "❌ Скасовано"
        else:
            status_text = status

        text += (
            f"🛒 <b>{name}</b>\n"
            f"💰 {price} USDT\n"
            f"📅 {date}\n"
            f"📌 {status_text}\n\n"
        )

    await callback.message.edit_text(
        text,
        reply_markup=main_menu
    )

    await callback.answer()
@router.callback_query(F.data == "catalog")
async def open_catalog(callback: CallbackQuery):

    await callback.message.edit_text(
        "📂 <b>Каталог товарів</b>\n\n"
        "Оберіть категорію:",
        reply_markup=catalog_menu
    )

    await callback.answer()    
@router.callback_query(F.data == "home")
async def back_home(callback: CallbackQuery):

    from keyboards.main import main_menu

    await callback.message.edit_text(
        "👋 <b>Ласкаво просимо до Samurai Shop!</b>\n\n"
        "Оберіть потрібний розділ:",
        reply_markup=main_menu
    )

    await callback.answer()   