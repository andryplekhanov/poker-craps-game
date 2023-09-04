from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline_blackjack import blackjack_start_game
from tgbot.keyboards.reply import blackjack_game_actions
from tgbot.services.blackjack_service import create_deck
from tgbot.services.printer import print_blackjack_rules


async def blackjack(message: Message, state: FSMContext):
    """
    Хендлер, реагирующий на команду /blackjack.
    Показывает правила игры и выдает кнопку - Начать игру.
    """
    await state.finish()
    await print_blackjack_rules(message)
    await message.answer('Ну что, сразимся?', reply_markup=await blackjack_start_game())


async def start_blackjack(call: CallbackQuery, state: FSMContext):
    """
    Хендлер, начинающий игру. Реагирует на нажатие инлайн-кнопки gallows_start_game.
    Вызывает функцию choose_word и получает слово.
    Записывает состояния игры good_letters, bad_letters, errors и word,
    затем вызывает состояние wait_letter и ожидает ввод буквы.
    """
    await call.message.edit_reply_markup(reply_markup=None)
    deck = await create_deck()
    async with state.proxy() as data:
        data['deck'] = deck

    await call.message.answer(f"👍 Начинаем новую игру.\n", reply_markup=blackjack_game_actions)
    await call.message.delete()


# async def give_up_blackjack(message: Message, state: FSMContext):
#     """
#     Хендлер, реагирующий на нажатие текстовой кнопки 'Сдаться и остановить игру'.
#     Вызывает функцию завершения игры finish_blackjack_game с победой бота.
#     """
#     await finish_blackjack_game(message, state, 'bot')


async def show_rules_blackjack(message: Message):
    """
    Хендлер, реагирующий на нажатие текстовой кнопки 'Правила игры'.
    Показывает правила игры.
    """
    await print_blackjack_rules(message)


def register_blackjack(dp: Dispatcher):
    dp.register_message_handler(blackjack, commands=["blackjack"], state="*")
    dp.register_callback_query_handler(start_blackjack, text='blackjack_start_game', state="*")
    # dp.register_message_handler(give_up_blackjack, Text(equals='⛔️ Сдаюсь ⛔️'), state="*")
    dp.register_message_handler(show_rules_blackjack, Text(equals='🔎 Подсмотреть правила 🔎'), state="*")
