from asyncio import sleep

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline_fool import fool_start_game
from tgbot.services.fool_service import create_deck, play_fool_round, hand_out_cards, pick_card
from tgbot.services.printer import print_fool_rules


async def fool(message: Message, state: FSMContext):
    """
    Хендлер, реагирующий на команду /fool.
    Показывает правила игры и выдает кнопку - Начать игру.
    """
    await state.finish()
    await print_fool_rules(message)
    await message.answer('Ну что, сразимся?', reply_markup=await fool_start_game())


async def start_fool(call: CallbackQuery, state: FSMContext):
    """
    Хендлер, начинающий игру. Реагирует на нажатие инлайн-кнопки fool_start_game.
    Задаёт начальные состояния и вызывает новый раунд play_fool_round.
    """
    await call.message.edit_reply_markup(reply_markup=None)
    deck = await create_deck()
    async with state.proxy() as data:
        data['deck'] = deck
    trump = await pick_card(state)
    player_cards = await hand_out_cards(state, 6)
    bot_cards = await hand_out_cards(state, 6)
    async with state.proxy() as data:
        data['player_cards'] = player_cards
        data['bot_cards'] = bot_cards
        data['trump'] = trump
    await call.message.answer(f"👍 Начинаем новую игру.\nПоехали!")
    await sleep(3)
    await play_fool_round(call.message, state)
    await call.message.delete()


def register_fool(dp: Dispatcher):
    dp.register_message_handler(fool, commands=["fool"], state="*")
    dp.register_callback_query_handler(start_fool, text='fool_start_game', state="*")
