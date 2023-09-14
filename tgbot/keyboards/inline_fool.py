from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.factories import for_fool_player_turn, for_fool_propose_more_cards_done, for_fool_player_cover
from tgbot.services.printer import RUS_CARDS_VALUES


async def check_players_card_for_cover(player_card: str, bot_card: str, trump: str) -> InlineKeyboardButton:
    """
    Функция проверяет карту ирока для создания кнопки.
    Если карта не подходит, чтобы ею покрыть карту бота, реакции на нажатие не будет.
    """
    if RUS_CARDS_VALUES[bot_card] < RUS_CARDS_VALUES[player_card] and player_card[-2] == bot_card[-2]:
        return InlineKeyboardButton(text=player_card, callback_data=for_fool_player_cover.new(card=player_card))
    elif player_card[-1] == trump[-1] and bot_card[-2] != trump[-2]:
        return InlineKeyboardButton(text=player_card, callback_data=for_fool_player_cover.new(card=player_card))
    return InlineKeyboardButton(text=player_card, callback_data='no_react')


async def prepare_big_keyboard(buttons: list, keyboard: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    """
    Функция разбивает инлайн-клавиатуру с большим количеством кнопок на насколько рядов по 6 кнопок.
    """
    keyboard.row(*buttons[:6])
    if len(buttons) > 6:
        keyboard.row(*buttons[6:12])
    if len(buttons) > 12:
        keyboard.row(*buttons[12:18])
    if len(buttons) > 18:
        keyboard.row(*buttons[18:24])
    return keyboard


async def fool_start_game() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - Начало игры Дурак
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='♣️ Играем ♠️', callback_data='fool_start_game'))
    return keyboard


async def fool_player_turn(cards: list, action: str) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - карты игрока, чтобы сделать ход.
    """

    keyboard = InlineKeyboardMarkup(row_width=6)
    buttons = list()
    for card in cards:
        buttons.append(InlineKeyboardButton(text=card, callback_data=for_fool_player_turn.new(card=card, action=action)))
    result = await prepare_big_keyboard(buttons, keyboard)
    return result


async def propose_more_cards(cards: list, action: str) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - карты игрока, которые он может добавить боту в придачу.
    """

    keyboard = InlineKeyboardMarkup(row_width=6)
    buttons = list()
    for card in cards:
        buttons.append(InlineKeyboardButton(text=card, callback_data=for_fool_player_turn.new(card=card, action=action)))
    result = await prepare_big_keyboard(buttons, keyboard)
    result.add(InlineKeyboardButton(text='Готово', callback_data=for_fool_propose_more_cards_done.new(action=action)))
    return result


async def player_cover(player_cards: list, bot_card: str, trump: str) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - карты игрока, которыми он может покрыть карту бота.
    """

    keyboard = InlineKeyboardMarkup(row_width=6)
    buttons = list()
    for card in player_cards:
        buttons.append(await check_players_card_for_cover(card, bot_card, trump))
    result = await prepare_big_keyboard(buttons, keyboard)
    result.add(InlineKeyboardButton(text='Беру', callback_data='player_takes'))
    return result


async def show_done_button(action: str) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой Ok - у игрока больше нечего добавлять боту в придачу.
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='♣️ Ok ♠️',
                                      callback_data=for_fool_propose_more_cards_done.new(action=action)))
    return keyboard


async def show_next_button() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой Далее - игрок не желает больше добавлять карты боту в придачу.
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Далее', callback_data="next_fool_round"))
    return keyboard
