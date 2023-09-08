from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.factories import for_fool_player_turn, for_fool_player_give_more, for_fool_propose_more_cards_done


async def fool_start_game() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - Начало игры Дурак
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='♣️ Играем ♠️', callback_data='fool_start_game'))
    return keyboard


async def fool_player_turn(cards: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=6, inline_keyboard=[
        [InlineKeyboardButton(text=card, callback_data=for_fool_player_turn.new(card=card)) for card in cards],
    ])
    return keyboard


async def propose_more_cards(cards: list, action: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=6, inline_keyboard=[
        [
            InlineKeyboardButton(text=card,
                                 callback_data=for_fool_player_give_more.new(card=card, action=action))
            for card in cards
        ],
        [InlineKeyboardButton(text='Готово', callback_data=for_fool_propose_more_cards_done.new(action=action))]
    ])
    return keyboard


async def show_done_button(action: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='♣️ Ok ♠️',
                                      callback_data=for_fool_propose_more_cards_done.new(action=action)))
    return keyboard


async def fool_bot_turn() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='♣️ Ok ♠️', callback_data='fool_bot_turn'))
    return keyboard
