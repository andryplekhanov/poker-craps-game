from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.keyboards.reply import main_actions
from tgbot.services.game import play_round


async def user_start(message: Message):
    await message.reply("Привет! Жми старт, чтобы бросить кубики и начать игру",
                        reply_markup=main_actions)


async def start_craps(message: Message, state: FSMContext):
    await state.finish()
    async with state.proxy() as data:
        data['round_counter'] = 1
    await play_round(message, state)


def register_start(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(start_craps, Text(contains='Start CRAPS'))
