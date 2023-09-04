from random import choice

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

DICES = {
    1: ' 1⃣ ',
    2: ' 2⃣ ',
    3: ' 3⃣ ',
    4: ' 4⃣ ',
    5: ' 5⃣ ',
    6: ' 6⃣ ',
}

GALLOWS = {
    1: '  _______\n  |/\n  |\n  |\n  |\n  |\n  |\n  |\n  |\n__|________\n|         |',
    2: '  _______\n  |/\n  |     ( )\n  |\n  |\n  |\n  |\n  |\n  |\n__|________\n|         |',
    3: '  _______\n  |/\n  |     ( )\n  |      |\n  |\n  |\n  |\n  |\n  |\n__|________\n|         |',
    4: '  _______\n  |/\n  |     ( )\n  |      |_\n  |        \ \n  |\n  |\n  |\n  |\n__|________\n|         |',
    5: '  _______\n  |/\n  |     ( )\n  |     _|_\n  |    /   \ \n  |\n  |\n  |\n  |\n__|________\n|         |',
    6: '  _______\n  |/\n  |     ( )\n  |     _|_\n  |    / | \ \n  |      | \n  |\n  |\n  |\n__|________\n|         |',
    7: '  _______\n  |/\n  |     ( )\n  |     _|_\n  |    / | \ \n  |      | \n  |     / \ \n  |    /   \ \n  |\n__|________\n|         |',
    8: '  _______\n  |/     |\n  |     (_)\n  |     _|_\n  |    / | \ \n  |      | \n  |     / \ \n  |    /   \ \n  |\n__|________\n|         |\n*** RIP ***',
}

HAPPY_EMOTIONS = [
    '👤 Я победил! Я победил этого человека! Вы это видели?',
    '👤 Да! Да! Да! Я выиграл!',
    '👤 А-ха-ха! Сасай, лалка! Я выиграл!',
    '👤 А-ха-ха! Ты продул! Даже твоя бабушка играла лучше!',
    '👤 Фуу... Ну ты и лох! Я выиграл!',
    '👤 Ты проиграл. Бывает. Давай ещё партию?',
    '👤 Ты проиграл. Не расстраивайся. Ещё партеечку?',
    '👤 Ты продул! Ты продул! А-ха-ха!',
    '👤 Это кто молодец? Я молодец! Я победил!',
    '👤 Партия за мной. Не хочешь взять реванш?',
    '👤 А-ха-ха! Иди домой, неудачник!',
    '👤 Ах ты ж мой приятный! Как я люблю, когда ты проигрываешь!',
    '👤 О, боты! Я выиграл! Наконец!',
    '👤 Лошара ми кантара... Знаешь такую песню?',
]

UNHAPPY_EMOTIONS = [
    '👤 Ты выиграл. Моё почтение!',
    '👤 О мой бот! Ты меня обыграл!',
    '👤 Ах ты ж... Ок, ты выиграл.',
    '👤 Ну ладно... Твоя взяла',
    '👤 Ты выиграл. Поздравляю!',
    '👤 Эта партия за тобой. Мои поздравления!',
    '👤 Твоя взяла. Жаль...',
    '👤 Блин, ты выиграл!',
    '👤 Хорошая игра! Достойная победа. Поздравляю!',
    '👤 Паразит! Ты сделал меня! Как тебе это удалось?',
    '👤 Ты... победил? Да как ты смеешь? Требую реванша!',
    '👤 Ах ты кожаный мешок! Ты меня переиграл!',
    '👤 Радуйся, ты победил! Но я всё равно круче! Сразимся ещё раз?',
]

SUITS = ['♠️', '♥️', '♣️', '♦️']

VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


async def print_dice(message: Message, dices: list[int]) -> None:
    result = ''.join([DICES[dice] for dice in dices])
    await message.answer(f'{result}')


async def print_emotion(message: Message, bot_win: bool) -> None:
    if bot_win:
        await message.answer(f'{choice(HAPPY_EMOTIONS)}')
    else:
        await message.answer(f'{choice(UNHAPPY_EMOTIONS)}')


async def print_craps_rules(message: Message) -> None:
    text = ('<b>Правила игры в Craps:</b>\n\n'
            '• Игра ведётся до 5 очков\n'
            '• Играют двое: ты и бот\n'
            '• Вы поочереди бросаете 5 кубиков\n'
            '• Ваша задача: выбросить комбинацию старше, чем у бота\n'
            '• Вы можете перебросить "плохие" кубики 1 раз за раунд\n\n'
            '<b>Возможные комбинации</b> (от старшей к младшей):\n'
            ' 5⃣ 5⃣ 5⃣ 5⃣ 5⃣ - Покер\n'
            ' 5⃣ 5⃣ 5⃣ 5⃣ 3⃣ - Карэ\n'
            ' 2⃣ 2⃣ 2⃣ 6⃣ 6⃣ - Фул-хаус\n'
            ' 2⃣ 3⃣ 4⃣ 5⃣ 6⃣ - Большой стрейт\n'
            ' 1⃣ 2⃣ 3⃣ 4⃣ 5⃣ - Малый стрейт\n'
            ' 2⃣ 2⃣ 2⃣ 6⃣ 1⃣ - Тройка\n'
            ' 5⃣ 5⃣ 3⃣ 3⃣ 6⃣ - Две пары\n'
            ' 4⃣ 4⃣ 1⃣ 2⃣ 3⃣ - Пара\n'
            ' 1⃣ 2⃣ 3⃣ 5⃣ 6⃣ - Ничего\n\n'
            '• Если у вас и у бота в итоге оказались одинаковые комбинации, то победа в раунде достается тому, '
            'у кого больше сумма кубиков. Например:\n'
            '🤵 Вы выбросили Тройку  2⃣ 2⃣ 2⃣ 4⃣ 5⃣  (сумма 6)\n'
            '👤 Бот выбросил Тройку  6⃣ 6⃣ 6⃣ 4⃣ 5⃣  (сумма 18)\n'
            'В этом случае победа достанется Боту\n\n'
            '• Если комбинации и суммы кубиков совпали, в раунде объявляется ничья.'
            )
    await message.answer(text, parse_mode='html')


async def print_gallows_rules(message: Message) -> None:
    text = ('<b>Правила игры в "Виселицу":</b>\n\n'
            'Всё просто: я загадываю слово, а ты его отгадываешь по буквам.\n\n'
            'Есть одно "но": играем на твою... 😱 жизнь.\n\n'
            'Сильно не переживай: ты можешь ошибиться аж 7 раз. Но 8-ая ошибка станет для тебя фатальной 💀.\n\n'
            'И ещё: здесь у нас не "Поле чудес". Буквы "и" и "й" - это разные буквы, так же как и "е" и "ё" 😈😈😈.'
            'Так же некоторые слова могут быть во множественном числе (вот это реально подстава) 😈😈😈.')
    await message.answer(text, parse_mode='html')


async def print_gallows_letter(message: Message, state: FSMContext) -> None:
    states = await state.get_data()
    good_letters = states.get('good_letters')
    word = states.get('word')
    text = [f' {letter} ' if letter in good_letters else ' * ' for letter in word]
    await message.answer(''.join(text))


async def print_gallows(message: Message, errors: int) -> None:
    await message.answer(f'<code>{GALLOWS[errors]}</code>', parse_mode='html')


async def print_correct_word(message: Message, state: FSMContext) -> None:
    states = await state.get_data()
    word = ''.join(states.get('word'))
    await message.answer(f'Я загадал слово <b>"{word}"</b>', parse_mode='html')


async def print_blackjack_rules(message: Message) -> None:
    text = ('<b>Правила игры в "Blackjack":</b>\n\n')
    await message.answer(text, parse_mode='html')


async def print_cards(message: Message, state: FSMContext, print_for: str) -> None:
    states = await state.get_data()
    cards = states.get('player_cards') if print_for == 'player' else states.get('bot_cards')
    result = ', '.join(cards) if print_for == 'player' else '🀄' * len(cards)
    await message.answer(result)
