from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def blackjack_start_game() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - Начало игры Blackjack
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='♣️ Играем ♠️', callback_data='blackjack_start_game'))
    return keyboard


async def blackjack_next_round() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - Начало игры Blackjack
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='♣️ Далее ... ♠️', callback_data='blackjack_next_round'))
    return keyboard


async def take_card() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - Взять карту
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Взять карту', callback_data='take_card'))
    return keyboard


async def bot_takes_card() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - Бот берёт карты
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Ок', callback_data='bot_takes_card'))
    return keyboard


async def blackjack_action_choice() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопками - "Взять ещё карту" и "Хватит"
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Ещё...', callback_data='take_card'))
    keyboard.add(InlineKeyboardButton(text='Хватит', callback_data='enough_card'))
    return keyboard

