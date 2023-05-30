from aiogram.dispatcher.filters.state import State, StatesGroup

class Expense(StatesGroup):
    category = State()
    subcategory = State()
    price = State()
    date = State()
    description = State()

class Income(StatesGroup):
    date = State()
    price = State()
    description = State()

class FetchFilters(StatesGroup):
    date = State()
    filter = State()
    category = State()
    subcategory = State()
