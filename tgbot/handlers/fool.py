from asyncio import sleep

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline_fool import fool_start_game, show_done_button
from tgbot.misc.factories import for_fool_player_turn, for_fool_propose_more_cards_done
from tgbot.services.fool_service import create_deck, play_fool_round, hand_out_cards, pick_card, place_card_on_desk, \
    bot_try_cover, check_who_first
from tgbot.services.printer import print_fool_rules


async def fool(message: Message, state: FSMContext):
    """
    Хендлер, реагирующий на команду /fool.
    Показывает правила игры и выдает кнопку - Начать игру.
    """
    await state.finish()
    await print_fool_rules(message)
    await message.answer('Ну что, сразимся?', reply_markup=await fool_start_game())


async def start_fool(call: CallbackQuery, state: FSMContext):
    """
    Хендлер, начинающий игру. Реагирует на нажатие инлайн-кнопки fool_start_game.
    Задаёт начальные состояния и вызывает новый раунд play_fool_round.
    """
    await call.message.edit_reply_markup(reply_markup=None)

    deck = await create_deck()
    async with state.proxy() as data:
        data['deck'] = deck

    trump = await pick_card(state)
    player_cards = await hand_out_cards(state, 6)
    bot_cards = await hand_out_cards(state, 6)
    who_first = await check_who_first(trump, player_cards, bot_cards)

    async with state.proxy() as data:
        data['player_cards'] = player_cards
        data['bot_cards'] = bot_cards
        data['trump'] = trump
        data['last_winner'] = who_first

    await call.message.answer(f"👍 Начинаем новую игру.\nПоехали!")
    await sleep(3)
    await play_fool_round(call.message, state)
    await call.message.delete()


async def player_put_card(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    card = callback_data.get('card')
    await place_card_on_desk(call.message, state, card, place_for='player')
    await call.message.answer(card)

    if callback_data.get('action') == 'cover':
        await bot_try_cover(call.message, state, card)
    else:
        await call.message.answer('🤵 Нету...', reply_markup=await show_done_button(action='next'))


async def player_propose_more_cards_done(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)

    states = await state.get_data()
    player_cards, bot_cards = states.get('player_cards'), states.get('bot_cards')
    new_player_cards = await hand_out_cards(state, 6 - len(player_cards))
    player_cards.extend(new_player_cards)

    if callback_data.get('action') in ['next', 'cover']:
        new_bot_cards = await hand_out_cards(state, 6-len(bot_cards))
        bot_cards.extend(new_bot_cards)
        last_winner = 'bot'
    else:
        desk = states.get('desk')
        bot_cards.extend(desk)
        last_winner = 'player'

    async with state.proxy() as data:
        data['last_winner'] = last_winner
        data['player_cards'] = player_cards
        data['bot_cards'] = bot_cards
    await play_fool_round(call.message, state)


def register_fool(dp: Dispatcher):
    dp.register_message_handler(fool, commands=["fool"], state="*")
    dp.register_callback_query_handler(start_fool, text='fool_start_game', state="*")
    dp.register_callback_query_handler(player_put_card, for_fool_player_turn.filter(), state="*")
    dp.register_callback_query_handler(player_propose_more_cards_done, for_fool_propose_more_cards_done.filter(), state="*")
