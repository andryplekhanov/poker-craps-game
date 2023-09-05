from asyncio import sleep
from random import choice
from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.inline_blackjack import take_card, bot_takes_card
from tgbot.services.printer import SUITS, VALUES, print_cards


async def create_deck() -> list[str]:
    return [f'{val}{suit}' for suit in SUITS for val in VALUES]


async def pick_card(state: FSMContext) -> Union[tuple[str, str], None]:
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


async def get_game_data(state: FSMContext) -> tuple[int, str, int, int]:
    states = await state.get_data()
    round_counter = states.get('round_counter')
    last_winner = states.get('last_winner')
    player_score = states.get('player_score')
    bot_score = states.get('bot_score')
    return round_counter, last_winner, player_score, bot_score


async def save_card(state: FSMContext, card, save_for: str) -> None:
    states = await state.get_data()
    cards = states.get('player_cards') if save_for == 'player' else states.get('bot_cards')
    cards.append(card)

    async with state.proxy() as data:
        if save_for == 'player':
            data['player_cards'] = cards
        else:
            data['bot_cards'] = cards


async def get_cards_points(cards: list) -> int:
    result = 0
    was_ace = False
    for card in cards:
        if card[0] == 'A' and not was_ace:
            was_ace = True
            if result <= 10:
                result += 11
            else:
                result += 1
        elif card[0] == 'A' and was_ace and result > 21:
            result -= 11
            result += 2
        elif card[0] == 'A' and (result >= 20 or was_ace):
            result += 1
        elif card[0] in ['J', 'Q', 'K'] or card[1] == '0':
            result += 10
        else:
            result += int(card[0])
    if was_ace and result > 21:
        result -= 11
        result += 1
    print(result)
    return result


async def play_blackjack_turn(message: Message, state: FSMContext) -> None:
    """
    Управляющая функция. Вызывает функцию броска кубиков roll_dice.
    Вызывает функцию проверки комбинации check_combination. Вызывает функцию печати кубиков print_dice.
    :return: кортеж: (mark: оценка, summa: сумма, result: название выпавшей комбинации, dice_list: список кубиков)
    """
    await sleep(2)
    card = await pick_card(state)
    if card:
        await save_card(state, card, save_for='player')
    await print_cards(message, state, print_for='player')
    # summa, result = await check_blackjack_combination(card)
    # await print_dice(message, dice_list)
    # return mark, summa, result, dice_list


async def bot_need_more(state: FSMContext) -> bool:
    states = await state.get_data()
    cards = states.get('bot_cards')
    print(cards)
    cards_points = await get_cards_points(cards)
    return cards_points < 17


async def play_blackjack_bot_turn(message: Message, state: FSMContext) -> None:
    """
    Управляющая функция. Вызывает функцию броска кубиков roll_dice.
    Вызывает функцию проверки комбинации check_combination. Вызывает функцию печати кубиков print_dice.
    :return: кортеж: (mark: оценка, summa: сумма, result: название выпавшей комбинации, dice_list: список кубиков)
    """
    await sleep(1)
    card = await pick_card(state)
    if card:
        await save_card(state, card, save_for='bot')
    if await bot_need_more(state):
        await play_blackjack_bot_turn(message, state)
    else:
        await message.answer('👤 Мне достаточно')


async def play_blackjack_round(message: Message, state: FSMContext) -> None:
    """
    Функция начинает новый раунд. Показывает сообщение с текущим счетом.
    В зависимости от того, кто победил в прошлом раунде - тому предлагает сделать ход нажатием на инлайн-кнопку.
    """
    round_counter, last_winner, player_score, bot_score = await get_game_data(state)
    await message.answer(f'🔔 РАУНД #{round_counter}\n'
                         f'Ты <b>{player_score}:{bot_score}</b> Я',
                         parse_mode='html')

    if last_winner is None or last_winner == 'player':
        await message.answer(f'🤵 Твой ход...', reply_markup=await take_card())
    else:
        await message.answer(f'👤 Мой ход...', reply_markup=await bot_takes_card())
