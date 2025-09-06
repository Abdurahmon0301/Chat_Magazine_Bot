from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_phone = State()
    waiting_for_address = State()
