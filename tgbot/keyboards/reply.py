from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура для выбора действия
main_actions = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="🎲 Начать игру 🎲")],
        [KeyboardButton(text="⛔️ Сдаться и остановить игру ⛔️")],
        [KeyboardButton(text="🔎 Правила игры 🔎")],
    ],
    one_time_keyboard=True
)
