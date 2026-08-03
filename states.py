from aiogram.fsm.state import State, StatesGroup


class AddProduct(StatesGroup):
    category = State()
    name = State()
    description = State()
    price = State()
    photo = State()
    content = State()


class AddStock(StatesGroup):
    product_id = State()
    content = State()

    from aiogram.fsm.state import State, StatesGroup


class Support(StatesGroup):
    message = State()

class ReplySupport(StatesGroup):
    message = State()