from asyncio import sleep
from random import choice
from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot.keyboards.inline_blackjack import take_card, bot_takes_card, blackjack_next_round
from tgbot.services.craps_service import reward_player, reward_bot
from tgbot.services.default_commands import get_default_commands
from tgbot.services.printer import SUITS, VALUES, print_cards, print_emotion


async def create_deck() -> list[str]:
    """
    Функция создаёт новую колоду карт. Возвращает список строк в формате ['A♣️', '7♦️', 'Q♠️'...]
    """
    return [f'{val}{suit}' for suit in SUITS for val in VALUES]


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


async def get_game_data(state: FSMContext) -> tuple[int, str, int, int]:
    """
    Функция обращается к машине состояний и берет необходимые данные:
    round_counter, last_winner, player_score, bot_score
    :return: round_counter, last_winner, player_score, bot_score
    """
    states = await state.get_data()
    round_counter = states.get('round_counter')
    last_winner = states.get('last_winner')
    player_score = states.get('player_score')
    bot_score = states.get('bot_score')
    return round_counter, last_winner, player_score, bot_score


async def save_card(state: FSMContext, card: str, save_for: str) -> None:
    """
    Функция добавляет карту к набору игрока или бота в машине состояний.
    """
    states = await state.get_data()
    cards = states.get('player_cards') if save_for == 'player' else states.get('bot_cards')
    cards.append(card)

    async with state.proxy() as data:
        if save_for == 'player':
            data['player_cards'] = cards
        else:
            data['bot_cards'] = cards


async def get_cards_points(cards: list) -> int:
    """
    Функция подсчитывает и возвращает очки в наборе карт.
    """
    result = 0
    ace_counter = 0
    for card in cards:
        if card[0] == 'A':
            ace_counter += 1
        elif card[0] in ['J', 'Q', 'K'] or card[1] == '0':
            result += 10
        else:
            result += int(card[0])

    if ace_counter > 0:
        if result > 10:
            result += ace_counter
        elif result == 10:
            if ace_counter == 1:
                result += 11
            else:
                result += ace_counter
        else:
            if ace_counter == 1:
                result += 11
            elif ace_counter == 2:
                result += 11
                result += 1
            elif ace_counter == 3 and result <= 8:
                result += 11
                result += 2
            elif ace_counter == 3 and result > 8:
                result += ace_counter
            elif ace_counter == 4 and result <= 7:
                result += 11
                result += 3
            elif ace_counter == 4 and result <= 7:
                result += ace_counter
    return result


async def play_blackjack_turn(message: Message, state: FSMContext) -> None:
    """
    Управляющая функция. Вызывает функцию выбора карты pick_card.
    Сохраняет карту save_card.
    Печатает карты игрока print_cards.
    """
    await sleep(1)
    card = await pick_card(state)
    if card:
        await save_card(state, card, save_for='player')
    states = await state.get_data()
    cards = states.get('player_cards')
    await print_cards(message, cards, print_as='open')


async def check_fairplay(state: FSMContext) -> bool:
    """
    Функция проверяет, не пытается ли игрок схитрить и забрать все карты из колоды.
    Если карт 12 или больше - возвращает False.
    """
    states = await state.get_data()
    cards = states.get('player_cards')
    return not len(cards) > 12


async def bot_need_more(state: FSMContext) -> bool:
    """
    Функция проверяет, нужно ли боту брать ещё карту.
    Если у бота меньше 17 очков - нужно брать ещё.
    """
    states = await state.get_data()
    cards = states.get('bot_cards')
    cards_points = await get_cards_points(cards)
    return cards_points < 17


async def play_blackjack_bot_turn(message: Message, state: FSMContext) -> None:
    """
    Управляющая функция. Вызывает функцию взятия карты за бота pick_card. Сохраняет карту save_card.
    Вызывает функцию проверки необходимости брать ещё карту bot_need_more. Если нужно, вызывает рекурсивно саму себя.
    Иначе печатает ответ бота "Мне достаточно".
    """
    card = await pick_card(state)
    if card:
        await save_card(state, card, save_for='bot')
    if await bot_need_more(state):
        await play_blackjack_bot_turn(message, state)
    else:
        await message.answer('🤖 Мне достаточно')


async def inc_round_counter(state: FSMContext) -> None:
    """
    Функция увеличивает счетчик раундов на 1.
    """
    states = await state.get_data()
    round_counter = states.get('round_counter')
    round_counter += 1
    async with state.proxy() as data:
        data['round_counter'] = round_counter


async def set_blackjack_winner(message: Message, state: FSMContext) -> None:
    """
    Функция определяет победителя раунда и печатает результат.
    """
    await sleep(1)
    await message.answer('Ок, вскрываемся...')
    states = await state.get_data()
    player_cards = states.get('player_cards')
    bot_cards = states.get('bot_cards')
    player_points = await get_cards_points(player_cards)
    bot_points = await get_cards_points(bot_cards)

    await sleep(2)
    await message.answer(f"🤵 Твой результат: {'перебор' if player_points > 21 else player_points}\n"
                         f"{', '.join(player_cards)}")
    await message.answer(f"🤖 Мой результат: {'перебор' if bot_points > 21 else bot_points}\n"
                         f"{', '.join(bot_cards)}")

    await inc_round_counter(state)

    await sleep(2)
    if (22 > player_points > bot_points) or (player_points < 22 and bot_points >= 22):
        await reward_player(state)
        await message.answer('🤵 Ты победил', reply_markup=await blackjack_next_round())
    elif (22 > bot_points > player_points) or (bot_points < 22 and player_points >= 22):
        await reward_bot(state)
        await message.answer('🤖 Я победил', reply_markup=await blackjack_next_round())
    else:
        await message.answer('Ничья', reply_markup=await blackjack_next_round())


async def play_blackjack_round(message: Message, state: FSMContext) -> None:
    """
    Функция начинает новый раунд. Показывает сообщение с текущим счетом.
    В зависимости от того, кто победил в прошлом раунде - тому предлагает сделать ход нажатием на инлайн-кнопку.
    """
    round_counter, last_winner, player_score, bot_score = await get_game_data(state)
    deck = await create_deck()
    async with state.proxy() as data:
        data['deck'] = deck
        data['player_cards'] = []
        data['bot_cards'] = []
    await message.answer(f'🔔 РАУНД #{round_counter}\n'
                         f'Ты <b>{player_score}:{bot_score}</b> Я',
                         parse_mode='html')

    if last_winner is None or last_winner == 'player':
        await message.answer(f'🤵 Твой ход...', reply_markup=await take_card())
    else:
        await message.answer(f'🤖 Мой ход...', reply_markup=await bot_takes_card())


async def finish_blackjack(message: Message, state: FSMContext, winner: str) -> None:
    """
    Функция завершает игру.
    В зависимости от победителя печатает соответствующую эмоцию бота.
    Сбрасывает состояния игры и выводит меню с играми.
    """
    if winner == 'player':
        await print_emotion(message, False)
    else:
        await print_emotion(message, True)
    await state.finish()
    await sleep(3)
    commands = await get_default_commands()
    await message.answer(f"🤖 Во что сыграем?\n\n{commands}", reply_markup=ReplyKeyboardRemove())
