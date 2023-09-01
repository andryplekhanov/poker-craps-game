from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.default_commands import get_default_commands


async def print_help(message: Message) -> None:
    """
    Функция, реагирующая на команду 'help'.
    Выводит сообщение с описанием команд.
    """

    commands = await get_default_commands()
    await message.answer(f"Я реагирую на следующие команды:\n\n{commands}")


def register_help(dp: Dispatcher):
    dp.register_message_handler(print_help, commands=["help"], state="*")
