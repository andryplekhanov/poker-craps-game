from asyncio import sleep

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from tgbot.keyboards.inline_gallows import gallows_start_game
from tgbot.keyboards.reply import gallows_game_actions
from tgbot.misc.states import GallowsGame
from tgbot.services.default_commands import get_default_commands
from tgbot.services.gallows_service import choose_word, check_letter
from tgbot.services.printer import print_gallows_rules, print_emotion, print_gallows_letter


async def gallows(message: Message, state: FSMContext):
    """
    Хендлер, реагирующий на команду /gallows.
    Показывает правила игры и выдает кнопку - Начать игру.
    """
    await state.finish()
    await print_gallows_rules(message)
    await message.answer('Сыграем?', reply_markup=await gallows_start_game())


async def start_gallows(call: CallbackQuery, state: FSMContext):
    """
    Хендлер, начинающий игру. Реагирует на нажатие инлайн-кнопки gallows_start_game.
    Вызывает функцию choose_word и получает слово.
    Записывает состояния игры good_letters, bad_letters, errors и word,
    затем вызывает состояние wait_letter и ожидает ввод буквы.
    """
    await call.message.edit_reply_markup(reply_markup=None)
    word = await choose_word()
    word = word.rstrip('\n')
    print(word)
    async with state.proxy() as data:
        data['good_letters'] = list()
        data['bad_letters'] = list()
        data['errors'] = 0
        data['word'] = list(word)
    await call.message.answer(f"👍 Начинаем новую игру.\n"
                              f"Я загадал слово из {len(word)} букв. Отгадай его за 7 попыток.\n"
                              "Поехали!!!\nВведи букву...", reply_markup=gallows_game_actions)
    await print_gallows_letter(call.message, state)
    await GallowsGame.wait_letter.set()
    await call.message.delete()


async def get_letter(message: Message, state: FSMContext):
    """
    Хендлер,
    """

    letter = message.text
    if not letter.isalpha() or not len(letter) == 1:
        await message.answer('Вам нужно ввести 1 букву')
    else:
        await check_letter(message, state, letter)


async def give_up_gallows(message: Message, state: FSMContext):
    """
    Хендлер, реагирующий на нажатие текстовой кнопки 'Сдаться и остановить игру'.
    Сбрасывает все состояния. Показывает эмоциональную реакцию бота на победу.
    Показывает меню с командами.
    """
    states = await state.get_data()
    word = ''.join(states.get('word'))
    await message.answer(f'Я загадал слово <b>"{word}"</b>', parse_mode='html')
    await state.finish()
    await print_emotion(message=message, bot_win=True)
    await sleep(3)
    commands = await get_default_commands()
    await message.answer(f"Выбирай игру:\n\n{commands}", reply_markup=ReplyKeyboardRemove())


async def show_rules_gallows(message: Message):
    """
    Хендлер, реагирующий на нажатие текстовой кнопки 'Правила игры'.
    Показывает правила игры.
    """
    await print_gallows_rules(message)


def register_gallows(dp: Dispatcher):
    dp.register_message_handler(gallows, commands=["gallows"], state="*")
    dp.register_callback_query_handler(start_gallows, text='gallows_start_game', state="*")
    dp.register_message_handler(give_up_gallows, Text(equals='⛔️ Сдаться ⛔️'), state="*")
    dp.register_message_handler(show_rules_gallows, Text(equals='🔎 Правила 🔎'), state="*")
    dp.register_message_handler(get_letter, state=GallowsGame.wait_letter),
