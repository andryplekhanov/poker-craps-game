from asyncio import sleep
from collections import Counter
from random import randint

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.services.printer import print_dice


async def roll_dice() -> list[int]:
    return [randint(1, 6) for _ in range(5)]


async def check_combination(dice_set: list[int]) -> tuple[int, int, str]:
    combination_dict = Counter(dice_set)  # {5: 4, 6: 1}
    combination_dict_values = sorted(list(combination_dict.values()), reverse=True)  # [4, 1]

    if combination_dict_values[0] == 5:
        mark = 10
        summa = sum(dice_set)
        result = 'Poker'
    elif combination_dict_values[0] == 4:
        mark = 9
        summa = sum([key * val for key, val in combination_dict.items() if val == 4])
        result = 'Quads'
    elif combination_dict_values[0] == 3 and combination_dict_values[1] == 2:
        mark = 8
        summa = sum([key * val for key, val in combination_dict.items() if val == 3 or val == 2])
        result = 'Full house'
    elif sum(dice_set) == 20 and len(combination_dict_values) == 5:
        mark = 7
        summa = 20
        result = 'Big straight'
    elif sum(dice_set) == 15 and len(combination_dict_values) == 5:
        mark = 6
        summa = 15
        result = 'Small straight'
    elif combination_dict_values[0] == 3:
        mark = 5
        summa = sum([key * val for key, val in combination_dict.items() if val == 3])
        result = 'Set'
    elif combination_dict_values[0] == 2 and combination_dict_values[1] == 2:
        mark = 4
        summa = sum([key * val for key, val in combination_dict.items() if val == 2])
        result = 'Two pairs'
    elif combination_dict_values[0] == 2:
        mark = 3
        summa = sum([key * val for key, val in combination_dict.items() if val == 2])
        result = 'Pair'
    else:
        mark = 2
        summa = sum(dice_set)
        result = 'Nothing'
    return mark, summa, result


async def play_turn(message: Message):
    await sleep(2)
    dice_set = await roll_dice()
    mark, summa, result = await check_combination(dice_set)
    await print_dice(message, dice_set)
    return mark, summa, result


async def play_round(message: Message, state: FSMContext):
    states = await state.get_data()
    round_counter = states.get('round_counter')
    last_winner = states.get('last_winner')
    await message.answer(f'🔔 ROUND #{round_counter}')

    if last_winner is None or last_winner == 'player':
        await message.answer(f'🤵 Your turn...')
        player_mark, player_summa, player_result = await play_turn(message)
        await sleep(2)
        await message.answer(f'👤 My turn...')
        bot_mark, bot_summa, bot_result = await play_turn(message)
    else:
        await message.answer(f'👤 My turn...')
        bot_mark, bot_summa, bot_result = await play_turn(message)
        await sleep(2)
        await message.answer(f'🤵 Your turn...')
        player_mark, player_summa, player_result = await play_turn(message)
    await message.answer(f"🤵 Your result: {player_result} ({player_summa})\n"
                         f"👤 My result: {bot_result} ({bot_summa})")