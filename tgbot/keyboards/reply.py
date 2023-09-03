from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

craps_game_actions = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="⛔️ Сдаться и остановить игру ⛔️")],
        [KeyboardButton(text="🔎 Правила игры 🔎")],
    ],
    one_time_keyboard=True
)


gallows_game_actions = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="⛔️ Сдаться ⛔️")],
        [KeyboardButton(text="🔎 Правила 🔎")],
    ],
    one_time_keyboard=True
)
