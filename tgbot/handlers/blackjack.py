from asyncio import sleep

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline_blackjack import blackjack_start_game, blackjack_action_choice, take_card, bot_takes_card
from tgbot.keyboards.reply import blackjack_game_actions
from tgbot.services.blackjack_service import create_deck, play_blackjack_round, play_blackjack_turn, \
    play_blackjack_bot_turn
from tgbot.services.printer import print_blackjack_rules, print_cards


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
    Хендлер, начинающий игру. Реагирует на нажатие инлайн-кнопки blackjack_start_game.
    Вызывает функцию choose_word и получает слово.
    Записывает состояния игры good_letters, bad_letters, errors и word,
    затем вызывает состояние wait_letter и ожидает ввод буквы.
    """
    await call.message.edit_reply_markup(reply_markup=None)
    deck = await create_deck()
    async with state.proxy() as data:
        data['deck'] = deck
        data['round_counter'] = 1
        data['player_score'] = 0
        data['bot_score'] = 0
        data['player_cards'] = []
        data['bot_cards'] = []
    await call.message.answer(f"👍 Начинаем новую игру.\nИграем до 5 очков. Поехали!",
                              reply_markup=blackjack_game_actions)
    await sleep(3)
    await play_blackjack_round(call.message, state)
    await call.message.delete()


async def player_takes_card(call: CallbackQuery, state: FSMContext):
    """
    Хендлер, реагирующий на нажатие инлайн-кнопки 'do_roll' - осуществляет бросок кубиков за игрока.
    Вызывает управляющую функцию play_turn, получает результат и сохраняет его с помощью функции save_result.
    Далее проверяет, чей сейчас ход и предлагает боту либо совершить свой бросок,
    либо (если бот уже бросал) перебросить кубики.
    """
    await call.message.edit_reply_markup(reply_markup=None)
    await play_blackjack_turn(call.message, state)
    await call.message.answer(f"Берёшь еще?", reply_markup=await blackjack_action_choice())
    await call.message.delete()


async def player_enough_card(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    states = await state.get_data()
    last_winner = states.get('last_winner')
    if last_winner is None or last_winner == 'player':
        await call.message.answer(f'👤 Мой ход...', reply_markup=await bot_takes_card())
    else:
        pass
    await call.message.delete()


async def bot_take_card(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await play_blackjack_bot_turn(call.message, state)
    await print_cards(call.message, state, print_for='bot')

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
    dp.register_callback_query_handler(player_takes_card, text='take_card', state="*")
    dp.register_callback_query_handler(player_enough_card, text='enough_card', state="*")
    dp.register_callback_query_handler(bot_take_card, text='bot_takes_card', state="*")
