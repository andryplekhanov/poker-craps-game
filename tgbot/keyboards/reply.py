from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура для выбора действия
main_actions = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="🎲 Start CRAPS 🎲")],
        [KeyboardButton(text="⛔️ stop game ⛔️")],
        [KeyboardButton(text="🔎 help 🔎")],
    ],
    one_time_keyboard=True
)
