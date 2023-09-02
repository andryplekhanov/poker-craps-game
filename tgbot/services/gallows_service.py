import os
from random import choice


async def choose_word() -> str:
    """
    Функция читает слова из файла и выбирает случайное слово
    :return (str): случайное слово
    """
    path = os.path.abspath(os.path.join('tgbot', 'files', 'words.txt'))
    with open(path, 'r') as file:
        content = file.readlines()
        return choice(content)
