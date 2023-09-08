from asyncio import sleep
from random import choice
from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.inline_fool import fool_player_turn, fool_bot_turn, propose_more_cards, show_done_button, \
    player_cover
from tgbot.services.printer import RUS_CARDS_VALUES, print_fool_desk


async def create_deck() -> list[str]:
    """
    Функция создаёт новую колоду карт. Возвращает список строк в формате ['Т♣️', 'Д♦️', '6♠️'...]
    """
    return list(RUS_CARDS_VALUES.keys())


async def check_who_first(trump: str, player_cards: list[str], bot_cards: list[str]) -> str:
    players_trumps = [player_card for player_card in player_cards if player_card[-1] == trump[-1]]
    bots_trumps = [bot_card for bot_card in bot_cards if bot_card[-1] == trump[-1]]

    if players_trumps and bots_trumps:
        players_trumps_values = [RUS_CARDS_VALUES[card] for card in players_trumps]
        bots_trumps_values = [RUS_CARDS_VALUES[card] for card in bots_trumps]
        if min(bots_trumps_values) < min(players_trumps_values):
            return 'bot'
        else:
            return 'player'
    elif players_trumps and not bots_trumps:
        return 'player'
    elif bots_trumps and not players_trumps:
        return 'bot'
    else:
        return choice(['player', 'bot'])


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
    cards = [await pick_card(state) for _ in range(num)]
    return [card for card in cards if card is not None]


async def place_card_on_desk(message: Message, state: FSMContext, card: str, place_for: str) -> None:
    states = await state.get_data()
    desk = states.get('desk')
    desk.append(card)

    if place_for == 'player':
        cards = states.get('player_cards')
    else:
        cards = states.get('bot_cards')
    cards.remove(card)

    async with state.proxy() as data:
        if place_for == 'player':
            data['player_cards'] = cards
        else:
            data['bot_cards'] = cards
        data['desk'] = desk


async def bot_choose_card_for_cover(state: FSMContext, card: str) -> Union[str, None]:
    """
    Функция решает, какой картой бот должен покрыть карту игрока.
    Возвращает карту в формате строки '10♣' или None (если крыть нечем или бот не хочет крыть).
    """
    states = await state.get_data()
    bot_cards = states.get('bot_cards')  # ['10♣', '7♠', '8♦', '9♣', 'Д♠', '7♣']
    trump = states.get('trump')  # '9♠'
    deck = states.get('deck')
    player_value = RUS_CARDS_VALUES[card]  # 8
    player_suit = card[-1]  # '♣'

    if player_suit == trump[-1] and player_value in [11, 12, 13, 14] and len(deck) > 6:  # Если игрок сходил козырем и карта игрока == В, Д, К, Т и в колоде больше 6 карт, то бот не кроет карту
        return None

    # Ищем карты (не козыри), чтобы покрыть карту игрока.
    cards_for_cover = [
        bot_card for bot_card in bot_cards
        if (bot_card[-1] == player_suit and RUS_CARDS_VALUES[bot_card] > player_value)
    ]  # ['10♣', '9♣'] Здесь только те карты, которые совпадают по масти с картой игрока, и которые больше её по значению
    if cards_for_cover:
        cards_for_cover_values = [RUS_CARDS_VALUES[bot_card] for bot_card in cards_for_cover]  # [10, 9]
        card_for_cover = [bot_card for bot_card in cards_for_cover
                          if RUS_CARDS_VALUES[bot_card] == min(cards_for_cover_values)]  # ['9♣']
        if player_suit == trump[-1] and RUS_CARDS_VALUES[card_for_cover[0]] in [12, 13, 14] and len(deck) > 6:  # Если игрок сходил козырем и бот может покрыть его только Д, К, Т и в колоде более 6 карт, то бот не кроет карту
            return None
        return card_for_cover[0]
    else:  # Если не нашлось карты
        if player_suit == trump[-1]:  # Если игрок сходил козырем и бот не нашел карту, чтобы его покрыть
            return None
        trumps_for_cover = [bot_card for bot_card in bot_cards if bot_card[-1] == trump[-1]]  # ['7♠', 'Д♠'] Если игрок сходил НЕ козырем и бот не нашел обычную карту, чтобы его покрыть, то бот ищет козыри
        if trumps_for_cover:  # Если бот нашел козырь
            trumps_for_cover_values = [RUS_CARDS_VALUES[trump_for_cover] for trump_for_cover in trumps_for_cover]  # [7, 12]
            if len(deck) > 5 and all([trump_value in [12, 13, 14] for trump_value in trumps_for_cover_values]):  # Если в колоде больше 5 карт и все козыри бота == Д, К, Т, то бот не кроет карту
                return None
            trump_for_cover = [bot_card for bot_card in trumps_for_cover
                               if RUS_CARDS_VALUES[bot_card] == min(trumps_for_cover_values)]  # ['7♠']
            return trump_for_cover[0]  # Возвращает минимальный козырь
        else:  # Если бот нашел козырь, то крыть нечем
            return None


async def bot_choose_card(state: FSMContext) -> Union[str, None]:
    states = await state.get_data()
    bot_cards = states.get('bot_cards')  # ['10♣', '7♠', '8♦', '9♥', 'Д♠', '7♣']
    trump = states.get('trump')  # '9♠'

    if not bot_cards:
        return None

    common_cards = [card for card in bot_cards if card[-1] != trump[-1]]  # ['10♣', '8♦', '9♥', '7♣']
    if common_cards:
        common_cards_values = [RUS_CARDS_VALUES[card] for card in common_cards]  # [10, 8, 9, 7]
        result = [card for card in common_cards if RUS_CARDS_VALUES[card] == min(common_cards_values)]  # ['7♣']
        return result[0]

    trump_cards = [card for card in bot_cards if card[-1] == trump[-1]]  # ['7♠', 'Д♠']
    trump_cards_values = [RUS_CARDS_VALUES[card] for card in trump_cards]  # [7, 12]
    result = [card for card in trump_cards if RUS_CARDS_VALUES[card] == min(trump_cards_values)]  # ['7♠']
    return result[0]


async def player_need_to_cover(message: Message, state: FSMContext, bot_card: str):
    states = await state.get_data()
    cards = states.get('player_cards')
    trump = states.get('trump')
    await message.answer('Чем будете крыть?',
                         reply_markup=await player_cover(player_cards=cards, bot_card=bot_card, trump=trump))


async def check_more_cards(state: FSMContext, check_for: str) -> Union[list, None]:
    states = await state.get_data()
    cards_on_desk = states.get('desk')
    cards = states.get('player_cards') if check_for == 'player' else states.get('bot_cards')
    values = [RUS_CARDS_VALUES[card] for card in cards_on_desk]
    result = [card for card in cards if RUS_CARDS_VALUES[card] in values]
    if result:
        return result
    else:
        return None


async def bot_try_cover(message: Message, state: FSMContext, card: str) -> None:
    card_for_cover = await bot_choose_card_for_cover(state, card)
    if card_for_cover:
        await place_card_on_desk(message, state, card_for_cover, 'bot')
        await message.answer(f'🤖 Крою {card_for_cover}\nЕсть ещё?')
        more_cards = await check_more_cards(state, 'player')
        await sleep(1)
        if more_cards is not None:
            await message.answer('Вы можете добавить эти карты',
                                 reply_markup=await propose_more_cards(cards=more_cards, action='cover'))
        else:
            await message.answer('🤵 Нету...', reply_markup=await show_done_button(action='next'))
    else:
        await message.answer(f'🤖 {card} беру. Есть ещё?')
        more_cards = await check_more_cards(state, 'player')
        await sleep(1)
        if more_cards is not None:
            await message.answer('Вы можете добавить эти карты',
                                 reply_markup=await propose_more_cards(cards=more_cards, action='add'))
        else:
            await message.answer('🤵 Нету...', reply_markup=await show_done_button(action='take'))


async def play_fool_round(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['desk'] = []
    await print_fool_desk(message, state)
    states = await state.get_data()

    if states.get('last_winner') == 'bot':
        await message.answer(f'🤖 Мой ход...', reply_markup=await fool_bot_turn())
    else:
        await message.answer(f'🤵 Твой ход...', reply_markup=await fool_player_turn(states.get('player_cards'), 'cover'))
