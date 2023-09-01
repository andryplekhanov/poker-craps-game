from random import choice

from aiogram.types import Message

DICES = {
    1: ' 1⃣ ',
    2: ' 2⃣ ',
    3: ' 3⃣ ',
    4: ' 4⃣ ',
    5: ' 5⃣ ',
    6: ' 6⃣ ',
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
    '👤 Это кто молодец? Я молодец!',
    '👤 Партия за мной. Не хочешь взять реванш?',
    '👤 А-ха-ха! Иди домой, неудачник!',
    '👤 Ах ты ж мой приятный! Как я люблю, когда ты проигрываешь!',
    '👤 О, боты! Я выиграл! Наконец!',
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


async def print_dice(message: Message, dices: list[int]) -> None:
    result = ''.join([DICES[dice] for dice in dices])
    await message.answer(f'{result}')


async def print_emotion(message: Message, bot_win: bool) -> None:
    if bot_win:
        await message.answer(f'{choice(HAPPY_EMOTIONS)}')
    else:
        await message.answer(f'{choice(UNHAPPY_EMOTIONS)}')


async def print_craps_rule(message: Message) -> None:
    await message.answer('Правила игры в Craps')
