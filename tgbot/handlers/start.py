from asyncio import sleep

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import bot_roll, do_roll, bot_reroll
from tgbot.keyboards.reply import main_actions
from tgbot.misc.factories import for_reroll, for_reroll_done
from tgbot.services.game import play_round, play_turn, ask_reroll, play_reroll, save_result, should_bot_reroll, \
    choose_dices_for_bots_reroll, set_winner


async def user_start(message: Message):
    await message.answer("Привет! Жми старт, чтобы начать игру", reply_markup=main_actions)


async def start_craps(message: Message, state: FSMContext):
    states = await state.get_data()
    if states.get('round_counter') is not None:
        await message.answer("Ты ещё не закончил эту игру. Сперва сдайся!", reply_markup=main_actions)
    else:
        await state.finish()
        async with state.proxy() as data:
            data['round_counter'] = 1
            data['player_score'] = 0
            data['bot_score'] = 0
        await play_round(message, state)


async def players_roll(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    player_mark, player_summa, player_result, player_dice_list = await play_turn(call.message)
    await save_result(player_mark, player_summa, player_dice_list, save_for='player', state=state)
    await call.message.answer(f"🤵 Твой результат: <b>{player_result} ({player_summa})</b>", parse_mode='html')

    await sleep(2)

    states = await state.get_data()
    last_winner = states.get('last_winner')
    if last_winner is None or last_winner == 'player':
        await call.message.answer(f'👤 Мой бросок...', reply_markup=await bot_roll())
    else:
        await call.message.answer(f'👤 Теперь мой черёд...', reply_markup=await bot_reroll())


async def bots_roll(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    bot_mark, bot_summa, bot_result, bot_dice_list = await play_turn(call.message)
    await save_result(bot_mark, bot_summa, bot_dice_list, save_for='bot', state=state)
    await call.message.answer(f"👤 Мой результат: <b>{bot_result} ({bot_summa})</b>", parse_mode='html')

    await sleep(2)

    states = await state.get_data()
    last_winner = states.get('last_winner')
    if last_winner == 'bot':
        await call.message.answer(f'🤵 Твой бросок...', reply_markup=await do_roll())
    else:
        await ask_reroll(call.message, state)


async def bots_reroll(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    is_reroll = await should_bot_reroll(call.message, state)
    if is_reroll:
        await call.message.answer(f"👤 Я перебрасываю...")
        dices_for_bots_reroll = await choose_dices_for_bots_reroll(call.message, state)
        if dices_for_bots_reroll == 'all':
            bot_mark, bot_summa, bot_result, bot_dice_list = await play_turn(call.message)
        else:
            bot_mark, bot_summa, bot_result, bot_dice_list = await play_reroll(call.message, state, 'bot')
        await save_result(bot_mark, bot_summa, bot_dice_list, save_for='bot', state=state)
        await call.message.answer(f"👤 Мой результат: <b>{bot_result} ({bot_summa})</b>", parse_mode='html')

    states = await state.get_data()
    if states.get('last_winner') == 'bot':
        await ask_reroll(call.message, state)
    else:
        await set_winner(call.message, state)


async def get_dice_for_reroll(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    dice_value = callback_data.get('dice_value')
    states = await state.get_data()
    player_dice_list = states.get('player_dice_list')
    player_dice_list.remove(int(dice_value))
    async with state.proxy() as data:
        data['player_dice_list'] = player_dice_list
    await ask_reroll(call.message, state)
    await call.message.delete()


async def reroll_done(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    states = await state.get_data()

    if callback_data.get('action') == 'reroll_done':
        player_mark, player_summa, player_result, player_dice_list = await play_reroll(call.message, state, 'player')
    else:
        player_mark, player_summa, player_result, player_dice_list = await play_turn(call.message)
    await save_result(player_mark, player_summa, player_dice_list, save_for='player', state=state)

    await call.message.answer(f"🤵 Твой результат: <b>{player_result} ({player_summa})</b>", parse_mode='html')
    await sleep(2)

    if states.get('last_winner') == 'bot':
        await set_winner(call.message, state)
    else:
        await call.message.answer(f'👤 Теперь мой черёд...', reply_markup=await bot_reroll())


async def next_round(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    states = await state.get_data()
    round = states.get('round_counter')
    round += 1
    async with state.proxy() as data:
        data['round_counter'] = round
    await play_round(call.message, state)


def register_start(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(start_craps, Text(contains='Начать игру'))
    dp.register_callback_query_handler(players_roll, text='do_roll', state="*")
    dp.register_callback_query_handler(reroll_done, for_reroll_done.filter(), state="*")
    dp.register_callback_query_handler(next_round, text='next_round', state="*")
    dp.register_callback_query_handler(bots_roll, text='bot_roll', state="*")
    dp.register_callback_query_handler(bots_reroll, text='bot_reroll', state="*")
    dp.register_callback_query_handler(get_dice_for_reroll, for_reroll.filter(), state="*"),
