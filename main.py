import asyncio
import logging

from decouple import config
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

BOT_TOKEN = config('BOT_TOKEN')


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class CreateShippingStates(StatesGroup):
    Description = State()  # Состояние для описания груза
    Weight = State()  # Состояние для веса груза
    Status = State()  # Состояние для габаритов груза
    PickupAddress = State()  # Состояние для адреса отправки
    DeliveryAddress = State()  # Состояние для адреса получения
    PaymentMethod = State()  # Состояние для способа оплаты


@dp.message(CommandStart())
async def handle_start(message: types.Message,state: FSMContext):
    await message.answer(text=f'Hello {message.from_user.full_name}')
    await state.clear()



@dp.message(Command('help'))
async def handle_help(message: types.Message,state: FSMContext):
    await message.reply(text="Я помощник")
    await state.clear()


@dp.message(Command('create_shipping'))
async def create_shipping(message: types.Message,state: FSMContext):
    await message.answer("Готов начать создание накладной.\nВведите описание груза.")
    await state.set_state(CreateShippingStates.Description) # Устанавливаем состояние на получение описания груза

@dp.message(CreateShippingStates.Description)
async def set_description(message: types.Message, state: FSMContext):
    """
    Обработчик для получения описания накладной от клиента
    """
    if not message.text:
        await message.answer("Вы ввели что-то непонятное, нужно отправлять только текст")
        return
    await state.update_data(description=message.text)
    await message.answer("Введите вес груза.")
    await state.set_state(CreateShippingStates.Weight)  # Переходим к состоянию для веса груза

@dp.message(CreateShippingStates.Weight)
async def set_weight(message: types.Message, state: FSMContext):
    """
    Обработчик для получения веса накладной от клиента
    """
    if not message.text:
        await message.answer("Вы ввели что-то непонятное, нужно отправлять только текст")
        return
    await state.update_data(weight=message.text)
    await message.answer("Введите вес груза.")
    await state.set_state(CreateShippingStates.Status)  # Переходим к состоянию для статуса груза

@dp.message(CreateShippingStates.Status)
async def set_status(message: types.Message, state: FSMContext):
    """
    Обработчик для получения статуса накладной от клиента
    """
    if not message.text:
        await message.answer("Вы ввели что-то непонятное, нужно отправлять только текст")
        return
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(str(data))
    await state.set_state(CreateShippingStates.Weight)  # Переходим к состоянию для чего-то груза

@dp.message()
async def echo_message(message: types.Message):
    await message.answer(text=message.text)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
