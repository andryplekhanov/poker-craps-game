from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.keyboards.reply import main_actions
from tgbot.services.dice import DiceSet
from tgbot.services.game import Game
from tgbot.services.player import Player


async def user_start(message: Message):
    await message.reply("Hello, user!", reply_markup=main_actions)


async def start_craps(message: Message):
    player = Player(name='Andrey')
    comp = Player(name='Computer')
    dice_set = DiceSet()
    game = Game(player=player, computer=comp, dices=dice_set)
    round_counter = 1
    await message.answer(f"start)


def register_start(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(start_craps, Text(contains='Start CRAPS'))
