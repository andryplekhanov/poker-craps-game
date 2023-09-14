from asyncio import sleep

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from tgbot.keyboards.inline_fool import fool_start_game, show_done_button, propose_more_cards
from tgbot.keyboards.reply import fool_game_actions
from tgbot.misc.factories import for_fool_player_turn, for_fool_propose_more_cards_done, for_fool_player_cover
from tgbot.services.default_commands import get_default_commands
from tgbot.services.fool_service import create_deck, play_fool_round, hand_out_cards, pick_card, place_card_on_desk, \
    bot_try_cover, check_who_first, bot_turn, bot_add_all, add_cards_to_player, bot_full_up, player_full_up, \
    add_cards_to_bot, check_more_cards
from tgbot.services.printer import print_fool_rules, print_emotion


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

    deck = await create_deck()  # создаём колоду
    async with state.proxy() as data:
        data['deck'] = deck
        data['trump_used'] = False  # козырь на столе (не использован)

    trump = await pick_card(state)
    player_cards = await hand_out_cards(state, 6)
    bot_cards = await hand_out_cards(state, 6)
    who_first = await check_who_first(trump, player_cards, bot_cards)

    async with state.proxy() as data:
        data['player_cards'] = player_cards
        data['bot_cards'] = bot_cards
        data['trump'] = trump
        data['last_winner'] = who_first

    await call.message.answer(f"👍 Начинаем новую игру.\nПоехали!", reply_markup=fool_game_actions)
    await sleep(3)
    await play_fool_round(call.message, state)
    await call.message.delete()


async def player_put_card(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Хендлер, реагирующий на нажатие карты, когда игрок делает ход.
    В зависимости от ситуации (callback_data.get('action')), бот будет пытаться покрыть карту, либо будет брать.
    """
    await call.message.edit_reply_markup(reply_markup=None)
    card = callback_data.get('card')
    await place_card_on_desk(state, card, place_for='player')
    await call.message.answer(card)

    if callback_data.get('action') == 'cover':
        await bot_try_cover(call.message, state, card)
    else:
        await call.message.answer(f'🤖 {card} беру. Есть ещё?')
        more_cards = await check_more_cards(state, 'player')
        await sleep(1)
        if more_cards is not None:
            await call.message.answer('Вы можете добавить эти карты',
                                      reply_markup=await propose_more_cards(cards=more_cards, action='add'))
        else:
            await call.message.answer('🤵 Нету...', reply_markup=await show_done_button(action='take'))


async def player_covers(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Хендлер, реагирующий на нажатие карты, когда игрок кроет карту бота.
    """
    await call.message.edit_reply_markup(reply_markup=None)
    card = callback_data.get('card')
    await place_card_on_desk(state, card, place_for='player')
    await call.message.answer(f'🤵 Крою: {card}')
    await bot_turn(call.message, state, target='add')


async def player_takes(call: CallbackQuery, state: FSMContext):
    """
    Хендлер, реагирующий на нажатие кнопки "Беру", когда игрок берёт карту бота.
    """
    await call.message.edit_reply_markup(reply_markup=None)
    cards = await bot_add_all(state)
    if cards:
        await call.message.answer(f"🤖 Вот тебе ещё: {', '.join(cards)}")
    await add_cards_to_player(state)

    await bot_full_up(state)
    await player_full_up(state)
    async with state.proxy() as data:
        data['last_winner'] = 'bot'
    await sleep(2)
    await play_fool_round(call.message, state)


async def player_propose_more_cards_done(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Хендлер, реагирующий на нажатие кнопки "Готово", когда игрок добавляет карты, чтобы их взял бот.
    В зависимости от ситуации (callback_data.get('action')), бот либо отбился (тогда он назначается победителем раунда),
    либо берёт карты себе.
    """
    await call.message.edit_reply_markup(reply_markup=None)
    await player_full_up(state)

    if callback_data.get('action') in ['next', 'cover']:
        await bot_full_up(state)
        last_winner = 'bot'
    else:
        await add_cards_to_bot(state)
        last_winner = 'player'

    async with state.proxy() as data:
        data['last_winner'] = last_winner
    await play_fool_round(call.message, state)


async def next_fool_round(call: CallbackQuery, state: FSMContext):
    """
    Хендлер, реагирующий на нажатие кнопки "Ок", после того, как игрок отбился от карт бота.
    """
    await call.message.edit_reply_markup(reply_markup=None)
    await bot_full_up(state)
    await player_full_up(state)
    await sleep(2)
    await play_fool_round(call.message, state)


async def give_up_fool(message: Message, state: FSMContext):
    """
    Хендлер, реагирующий на нажатие текстовой кнопки 'Сдаюсь'.
    Завершает игру с победой бота.
    """
    await print_emotion(message, True)
    await state.finish()
    await sleep(3)
    commands = await get_default_commands()
    await message.answer(f"🤖 Во что сыграем?\n\n{commands}", reply_markup=ReplyKeyboardRemove())


def register_fool(dp: Dispatcher):
    dp.register_message_handler(fool, commands=["fool"], state="*")
    dp.register_callback_query_handler(start_fool, text='fool_start_game', state="*")
    dp.register_message_handler(give_up_fool, Text(equals='⛔️ Сдаться и остаться в дураках ⛔️'), state="*")
    dp.register_callback_query_handler(player_takes, text='player_takes', state="*")
    dp.register_callback_query_handler(next_fool_round, text='next_fool_round', state="*")
    dp.register_callback_query_handler(player_covers, for_fool_player_cover.filter(), state="*")
    dp.register_callback_query_handler(player_put_card, for_fool_player_turn.filter(), state="*")
    dp.register_callback_query_handler(player_propose_more_cards_done, for_fool_propose_more_cards_done.filter(), state="*")
