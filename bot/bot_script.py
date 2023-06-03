from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from bot.management.dispatcher import Bot, dp
from main import find_address

class States(StatesGroup):
    input_address = State()
    choose_address = State()

@dp.message_handler(text="/start")
async def start_handler(message: Message):
    msg = "Привет!👋\n\nВведите адрес, для которого нужно узнать глобальные координаты"
    await message.answer(msg)
    await States.input_address.set()

@dp.message_handler(state = States.input_address)
async def input_address(message: Message, state: FSMContext):
    places, coords = find_address(message.text)
    async with state.proxy() as data:
        data["coords"] = coords
    keyboard = InlineKeyboardMarkup()
    msg = "Вот, что мы нашли по Вашему запросу.\n\nВыберите нужную точку.\n\n"
    for pl in places:
        keyboard.add(InlineKeyboardButton(text=pl, callback_data=str(places.index(pl))))
        msg += pl + "\n"
    await message.answer(text=msg, parse_mode="HTML", reply_markup=keyboard)
    await message.delete()
    await States.next()

@dp.callback_query_handler(state = States.choose_address)
async def choose_address(query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        coords = data["coords"]
    
    await query.message.delete()
    msg = f"Вот запрашиваемые Вами координаты:\n\n<code>{coords[int(query.data)]}</code>\n\n/start - начать заново"
    la, lo = map(float, coords[int(query.data)].split(","))
    await Bot.send_message(query.from_user.id, msg, "HTML")
    await Bot.send_location(query.from_user.id, la, lo)
    await States.next()