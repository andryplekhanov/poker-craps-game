from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def gallows_start_game() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - Начало игры Виселица
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='💀 Играем 💀', callback_data='gallows_start_game'))
    return keyboard
