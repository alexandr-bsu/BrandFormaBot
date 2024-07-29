from aiogram.filters.state import StatesGroup, State


class OrderSG(StatesGroup):
    mark = State()
    review = State()
    good_mark = State()