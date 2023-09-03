from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline_gallows import gallows_start_game
from tgbot.keyboards.reply import gallows_game_actions
from tgbot.misc.states import GallowsGame
from tgbot.services.gallows_service import choose_word, check_letter, check_gallows_game_status, finish_gallows_game
from tgbot.services.printer import print_gallows_rules, print_gallows_letter


async def gallows(message: Message, state: FSMContext):
    """
    Хендлер, реагирующий на команду /gallows.
    Показывает правила игры и выдает кнопку - Начать игру.
    """
    await state.finish()
    await print_gallows_rules(message)
    await message.answer('Ну что, проверим твои знания русского языка? Или ты забздел?',
                         reply_markup=await gallows_start_game())


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
    async with state.proxy() as data:
        data['good_letters'] = list()
        data['bad_letters'] = list()
        data['errors'] = 0
        data['word'] = list(word)
    await call.message.answer(f"👍 Начинаем новую игру.\n"
                              f"Я загадал слово из {len(word)} букв. Отгадай его.\n"
                              "Поехали!!!\nВведи букву...", reply_markup=gallows_game_actions)
    await print_gallows_letter(call.message, state)
    await GallowsGame.wait_letter.set()
    await call.message.delete()


async def get_letter(message: Message, state: FSMContext):
    """
    Хендлер, ожидающий ввод буквы. Если введенный символ - не буква, просит ввести букву.
    Если введенный символ - буква, вызывает функцию проверки буквы check_letter.
    В конце проверяет состояние игры функцией check_gallows_game_status.
    """

    letter = message.text
    if not letter.isalpha() or not len(letter) == 1:
        await message.answer('Вам нужно ввести 1 букву')
    else:
        await check_letter(message, state, letter)
    await check_gallows_game_status(message, state)


async def give_up_gallows(message: Message, state: FSMContext):
    """
    Хендлер, реагирующий на нажатие текстовой кнопки 'Сдаться и остановить игру'.
    Вызывает функцию завершения игры finish_gallows_game с победой бота.
    """
    await finish_gallows_game(message, state, 'bot')


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
