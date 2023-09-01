from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.factories import for_reroll, for_reroll_done
from tgbot.services.printer import DICES


async def craps_start_game() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - Начало игры Craps
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='🎲 Поехали 🎲', callback_data='craps_start_game'))
    return keyboard


async def do_next() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - следующий раунд
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='🎲 Далее 🎲', callback_data='next_round'))
    return keyboard


async def do_roll() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - бросить кубики
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='🎲 Бросить 🎲', callback_data='do_roll'))
    return keyboard


async def bot_roll() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - бот бросает кубики
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='🎲 Ok 🎲', callback_data='bot_roll'))
    return keyboard


async def bot_reroll() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - бот перебрасывает кубики
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='🎲 Ok 🎲', callback_data='bot_reroll'))
    return keyboard


async def players_reroll(player_dice_list: list) -> InlineKeyboardMarkup:
    """
    Клавиатура с выбором: какие кубики игрок желает перебросить
    """

    keyboard = InlineKeyboardMarkup(row_width=5, inline_keyboard=[
        [InlineKeyboardButton(text=DICES[dice], callback_data=for_reroll.new(dice_value=dice)) for dice in player_dice_list],
        [InlineKeyboardButton(text='Перебросить все', callback_data=for_reroll_done.new(action='reroll_all'))],
        [InlineKeyboardButton(text='Готово!', callback_data=for_reroll_done.new(action='reroll_done'))],
    ])
    return keyboard
