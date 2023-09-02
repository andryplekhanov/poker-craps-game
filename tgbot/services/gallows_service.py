import os
from random import choice

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.services.printer import print_gallows_letter


async def choose_word() -> str:
    """
    Функция читает слова из файла и выбирает случайное слово
    :return (str): случайное слово
    """
    path = os.path.abspath(os.path.join('tgbot', 'files', 'words.txt'))
    with open(path, 'r') as file:
        content = file.readlines()
        return choice(content)


async def get_current_states(state: FSMContext) -> tuple[list, list, list, int]:
    """
    Функция обращается к машине состояний и забирает данные из класса GallowsGame.
    :return (tuple): good_letters, bad_letters, word, errors
    """
    states = await state.get_data()
    good_letters = states.get('good_letters')
    bad_letters = states.get('bad_letters')
    word = states.get('word')
    errors = states.get('errors')
    return good_letters, bad_letters, word, errors


async def check_letter(message: Message, state: FSMContext, letter: str):
    good_letters, bad_letters, word, errors = await get_current_states(state)

    if letter in good_letters or letter in bad_letters:
        await message.answer('Ты уже называл эту букву. Введи другую...')
    elif letter in word:
        good_letters.append(letter)
        async with state.proxy() as data:
            data['good_letters'] = good_letters
    else:
        bad_letters.append(letter)
        errors += 1
        async with state.proxy() as data:
            data['bad_letters'] = bad_letters
            data['errors'] = errors
    await print_gallows_letter(message, state)