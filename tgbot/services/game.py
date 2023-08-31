from asyncio import sleep
from collections import Counter
from random import randint

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.inline import do_roll, bot_roll, players_reroll, do_next
from tgbot.keyboards.reply import main_actions
from tgbot.services.printer import print_dice, print_emotion


async def roll_dice(num: int = 5) -> list[int]:
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
    return mark, summa, result, dice_list


async def play_reroll(message: Message, state: FSMContext, play_for: str) -> tuple[int, int, str, list]:
    await sleep(2)
    states = await state.get_data()
    if play_for == 'player':
        player_dice_list = states.get('player_dice_list')
    else:
        player_dice_list = states.get('bot_dice_list')
    num = 5 - len(player_dice_list)
    dice_list = await roll_dice(num=num)
    result_dice_list = player_dice_list + dice_list
    mark, summa, result = await check_combination(result_dice_list)
    await print_dice(message, result_dice_list)
    return mark, summa, result, result_dice_list


async def ask_reroll(message: Message, state: FSMContext):
    states = await state.get_data()
    player_dice_list = states.get('player_dice_list')
    await message.answer('Выбирай, какие кубики желаешь перебросить и жми "Готово!"\n'
                         'Если никакие не хочешь перебрасывать, жми сразу "Готово!"',
                         reply_markup=await players_reroll(player_dice_list))


async def should_bot_reroll(message: Message, state: FSMContext) -> bool:
    """
    Функция определяет, должен ли бот перебрасывать кубики.
    :param message: aiogram.types.Message
    :param state: aiogram.dispatcher.FSMContext
    :return: bool
    """
    states = await state.get_data()
    last_winner = states.get('last_winner')
    player_mark = states.get('player_mark')
    player_summa = states.get('player_summa')
    bot_mark = states.get('bot_mark')
    bot_summa = states.get('bot_summa')

    if last_winner is None or last_winner == 'player':
        if (bot_mark == player_mark) and (bot_summa > player_summa):
            await message.answer(f'👤 Я решил не перебрасывать')
            return False
        elif bot_mark > player_mark:
            await message.answer(f'👤 Я решил не перебрасывать')
            return False
        return True

    if bot_mark >= 6:
        await message.answer(f'👤 Я решил не перебрасывать')
        return False
    return True


async def choose_dices_for_bots_reroll(message: Message, state: FSMContext) -> str:
    """
    Функция, определяющая, какие кубики бот должен сохранить, а какие перебросить.
    Перезаписывает состояние 'bot_dice_list' - кубики, которые не будут переброшены.
    Возвращает строку.
    :param message: aiogram.types.Message
    :param state: aiogram.dispatcher.FSMContext
    :return: str - 'all' - если бот решил перебросить все кубики; 'some' - если бот выбрал несколько кубиков для переброса
    """
    states = await state.get_data()
    bot_mark = states.get('bot_mark')
    bot_dice_list = states.get('bot_dice_list')  # [5, 4, 5, 6, 1]

    if bot_mark == 2:
        await message.answer(f'👤 Я решил перебросить все...')
        return 'all'

    combination_dict = Counter(bot_dice_list)  # {5: 2, 6: 1, 4: 1, 1: 1}
    dices_for_save = []

    if bot_mark == 3 or bot_mark == 4:
        for key, val in combination_dict.items():
            if val == 2:
                for dice in bot_dice_list:  # [5, 4, 5, 6, 1]
                    if dice == key:
                        dices_for_save.append(dice)
    elif bot_mark == 5:
        for key, val in combination_dict.items():
            if val == 3:
                for dice in bot_dice_list:  # [5, 4, 5, 6, 5]
                    if dice == key:
                        dices_for_save.append(dice)
    elif bot_mark == 9:
        for key, val in combination_dict.items():
            if val == 4:
                for dice in bot_dice_list:  # [5, 5, 5, 6, 5]
                    if dice == key:
                        dices_for_save.append(dice)

    async with state.proxy() as data:
        data['bot_dice_list'] = dices_for_save
    return 'some'


async def reward_player(state: FSMContext) -> None:
    states = await state.get_data()
    score = states.get('player_score')
    score += 1
    async with state.proxy() as data:
        data['player_score'] = score
        data['last_winner'] = 'player'


async def reward_bot(state: FSMContext) -> None:
    states = await state.get_data()
    score = states.get('bot_score')
    score += 1
    async with state.proxy() as data:
        data['bot_score'] = score
        data['last_winner'] = 'bot'


async def finish_game(message: Message, player_score: int, bot_score: int, state: FSMContext) -> None:
    await state.finish()
    await message.answer(f"🏁 Игра окончена со счётом:\n"
                         f"🤵 Ты <b>{player_score}:{bot_score}</b> Бот 👤", reply_markup=main_actions)
    if player_score > bot_score:
        await print_emotion(message=message, bot_win=False)
    else:
        await print_emotion(message=message, bot_win=True)


async def set_winner(message: Message, state: FSMContext) -> None:
    states = await state.get_data()
    player_mark = states.get('player_mark')
    player_summa = states.get('player_summa')
    bot_mark = states.get('bot_mark')
    bot_summa = states.get('bot_summa')

    if player_mark > bot_mark:
        await reward_player(state)
        text = '🤵 Ты выиграл. У тебя старше комбинация.'
    elif player_mark < bot_mark:
        await reward_bot(state)
        text = '👤 Я выиграл. У меня старше комбинация.'
    else:
        if player_summa > bot_summa:
            await reward_player(state)
            text = '🤵 Ты выиграл. У тебя больше сумма.'
        elif player_summa < bot_summa:
            await reward_bot(state)
            text = '👤 Я выиграл. У меня больше сумма.'
        else:
            text = 'Ничья.'
    await message.answer(text, reply_markup=await do_next())


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
