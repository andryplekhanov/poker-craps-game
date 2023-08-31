from asyncio import sleep
from collections import Counter
from random import randint

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.inline import do_roll, bot_roll, players_reroll
from tgbot.services.printer import print_dice


async def roll_dice(num=5) -> list[int]:
    return [randint(1, 6) for _ in range(num)]


async def save_result(mark: int, summa: int, dice_list: list, save_for: str, state: FSMContext) -> None:
    async with state.proxy() as data:
        if save_for == 'player':
            data['player_mark'] = mark
            data['player_summa'] = summa
            data['player_dice_list'] = dice_list
        else:
            data['bot_mark'] = mark
            data['bot_summa'] = summa
            data['bot_dice_list'] = dice_list


async def check_combination(dice_set: list[int]) -> tuple[int, int, str]:
    combination_dict = Counter(dice_set)  # {5: 4, 6: 1}
    combination_dict_values = sorted(list(combination_dict.values()), reverse=True)  # [4, 1]

    if combination_dict_values[0] == 5:
        mark = 10
        summa = sum(dice_set)
        result = 'Покер'
    elif combination_dict_values[0] == 4:
        mark = 9
        summa = sum([key * val for key, val in combination_dict.items() if val == 4])
        result = 'Карэ'
    elif combination_dict_values[0] == 3 and combination_dict_values[1] == 2:
        mark = 8
        summa = sum([key * val for key, val in combination_dict.items() if val == 3 or val == 2])
        result = 'Фул-хаус'
    elif sum(dice_set) == 20 and len(combination_dict_values) == 5:
        mark = 7
        summa = 20
        result = 'Большой стрейт'
    elif sum(dice_set) == 15 and len(combination_dict_values) == 5:
        mark = 6
        summa = 15
        result = 'Малый стрейт'
    elif combination_dict_values[0] == 3:
        mark = 5
        summa = sum([key * val for key, val in combination_dict.items() if val == 3])
        result = 'Тройка'
    elif combination_dict_values[0] == 2 and combination_dict_values[1] == 2:
        mark = 4
        summa = sum([key * val for key, val in combination_dict.items() if val == 2])
        result = 'Две пары'
    elif combination_dict_values[0] == 2:
        mark = 3
        summa = sum([key * val for key, val in combination_dict.items() if val == 2])
        result = 'Пара'
    else:
        mark = 2
        summa = sum(dice_set)
        result = 'Ничего'
    return mark, summa, result


async def play_turn(message: Message) -> tuple[int, int, str, list]:
    await sleep(2)
    dice_list = await roll_dice()
    mark, summa, result = await check_combination(dice_list)
    await print_dice(message, dice_list)
    await message.delete()
    return mark, summa, result, dice_list


async def play_reroll(message: Message, state: FSMContext) -> tuple[int, int, str, list]:
    await sleep(2)
    states = await state.get_data()
    player_dice_list = states.get('player_dice_list')
    num = 5 - len(player_dice_list)
    dice_list = await roll_dice(num=num)
    result_dice_list = player_dice_list + dice_list
    mark, summa, result = await check_combination(result_dice_list)
    await print_dice(message, result_dice_list)
    await message.delete()
    return mark, summa, result, result_dice_list


async def ask_reroll(message: Message, state: FSMContext):
    states = await state.get_data()
    player_dice_list = states.get('player_dice_list')
    await message.answer('Выбирай, какие кубики желаешь перебросить и жми "Готово!"',
                         reply_markup=await players_reroll(player_dice_list))


async def play_round(message: Message, state: FSMContext):
    states = await state.get_data()
    round_counter = states.get('round_counter')
    last_winner = states.get('last_winner')
    player_score = states.get('player_score')
    bot_score = states.get('bot_score')
    await message.answer(f'🔔 РАУНД #{round_counter}\n'
                         f'Ты <b>{player_score}:{bot_score}</b> Я',
                         parse_mode='html')

    if last_winner is None or last_winner == 'player':
        await message.answer(f'🤵 Твой бросок...', reply_markup=await do_roll())
    else:
        await message.answer(f'👤 Мой бросок...', reply_markup=await bot_roll())
