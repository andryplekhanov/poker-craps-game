from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def blackjack_start_game() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - Начало игры Blackjack
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='♣️ Играем ♠️', callback_data='blackjack_start_game'))
    return keyboard
