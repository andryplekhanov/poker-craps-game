from random import choice
from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.services.printer import RUS_VALUES, SUITS, print_fool_desk


async def create_deck() -> list[str]:
    """
    Функция создаёт новую колоду карт. Возвращает список строк в формате ['Т♣️', 'Д♦️', '6♠️'...]
    """
    return [f'{val}{suit}' for suit in SUITS for val in RUS_VALUES]


async def pick_card(state: FSMContext) -> Union[str, None]:
    """
    Функция случайным образом выбирает из колоды карту и возвращает её в виде строки в формате 'A♣️'.
    Карта из колоды удаляется.
    Если колода пуста, возвращает None.
    """
    states = await state.get_data()
    cards = states.get('deck')
    try:
        card = choice(cards)
        cards.remove(card)
        async with state.proxy() as data:
            data['deck'] = cards
        return card
    except IndexError:
        return None


async def hand_out_cards(state: FSMContext, num: int) -> list[str]:
    return [await pick_card(state) for _ in range(num)]


async def play_fool_round(message: Message, state: FSMContext) -> None:
    await print_fool_desk(message, state)
