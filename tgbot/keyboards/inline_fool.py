from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.factories import for_fool_player_turn, for_fool_propose_more_cards_done, for_fool_player_cover
from tgbot.services.printer import RUS_CARDS_VALUES


async def check_players_card_for_cover(player_card: str, bot_card: str, trump: str) -> InlineKeyboardButton:
    if RUS_CARDS_VALUES[bot_card] < RUS_CARDS_VALUES[player_card] and player_card[-1] == bot_card[-1]:
        return InlineKeyboardButton(text=player_card, callback_data=for_fool_player_cover.new(card=player_card))
    elif player_card[-1] == trump[-1] and bot_card[-1] != trump[-1]:
        return InlineKeyboardButton(text=player_card, callback_data=for_fool_player_cover.new(card=player_card))
    return InlineKeyboardButton(text=player_card, callback_data='no_react')


async def fool_start_game() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой - Начало игры Дурак
    """

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='♣️ Играем ♠️', callback_data='fool_start_game'))
    return keyboard


async def fool_player_turn(cards: list, action: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=6, inline_keyboard=[
        [InlineKeyboardButton(text=card, callback_data=for_fool_player_turn.new(card=card, action=action))
         for card in cards],
    ])
    return keyboard


async def propose_more_cards(cards: list, action: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=6, inline_keyboard=[
        [
            InlineKeyboardButton(text=card,
                                 callback_data=for_fool_player_turn.new(card=card, action=action))
            for card in cards
        ],
        [InlineKeyboardButton(text='Готово', callback_data=for_fool_propose_more_cards_done.new(action=action))]
    ])
    return keyboard


async def player_cover(player_cards: list, bot_card: str, trump: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=6, inline_keyboard=[
        [
            await check_players_card_for_cover(card, bot_card, trump) for card in player_cards
        ],
        # [InlineKeyboardButton(text='Беру', callback_data=for_fool_player_takes.new(action=action))]
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
