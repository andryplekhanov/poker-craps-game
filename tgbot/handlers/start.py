from asyncio import sleep

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import bot_roll, do_roll
from tgbot.keyboards.reply import main_actions
from tgbot.misc.factories import for_reroll
from tgbot.services.game import play_round, play_turn, ask_reroll


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
    async with state.proxy() as data:
        data['player_mark'] = player_mark
        data['player_summa'] = player_summa
        data['player_dice_list'] = player_dice_list
    await call.message.answer(f"🤵 Твой результат: <b>{player_result} ({player_summa})</b>", parse_mode='html')

    await sleep(2)

    states = await state.get_data()
    last_winner = states.get('last_winner')
    if last_winner is None or last_winner == 'player':
        await call.message.answer(f'👤 Мой бросок...', reply_markup=await bot_roll())
    else:
        pass


async def bots_roll(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    bot_mark, bot_summa, bot_result, bot_dice_list = await play_turn(call.message)
    async with state.proxy() as data:
        data['bot_mark'] = bot_mark
        data['bot_summa'] = bot_summa
        data['bot_dice_list'] = bot_dice_list
    await call.message.answer(f"👤 Мой результат: <b>{bot_result} ({bot_summa})</b>", parse_mode='html')

    await sleep(2)

    states = await state.get_data()
    last_winner = states.get('last_winner')
    if last_winner == 'bot':
        await call.message.answer(f'🤵 Твой бросок...', reply_markup=await do_roll())
    else:
        await ask_reroll(call.message, state)


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


def register_start(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(start_craps, Text(contains='Начать игру'))
    dp.register_callback_query_handler(players_roll, text='do_roll', state="*")
    dp.register_callback_query_handler(bots_roll, text='bot_roll', state="*")
    dp.register_callback_query_handler(get_dice_for_reroll, for_reroll.filter(), state="*"),
