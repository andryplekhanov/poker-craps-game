from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.services.default_commands import get_default_commands


async def user_start(message: Message, state: FSMContext):
    """
    Хендлер, реагирующий на команду /start
    Показывает приветственное сообщение с командами.
    """

    await state.finish()
    commands = await get_default_commands()
    await message.answer(f"Привет и добро пожаловать!\n\n"
                         f"Я реагирую на следующие команды:\n\n{commands}")


def register_start(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
