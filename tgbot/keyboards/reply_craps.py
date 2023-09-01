from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура для выбора действия
game_actions = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="⛔️ Сдаться и остановить игру ⛔️")],
        [KeyboardButton(text="🔎 Правила игры 🔎")],
    ],
    one_time_keyboard=True
)
