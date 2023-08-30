from aiogram.types import Message

DICES = {
    1: ' 1⃣ ',
    2: ' 2⃣ ',
    3: ' 3⃣ ',
    4: ' 4⃣ ',
    5: ' 5⃣ ',
    6: ' 6⃣ ',
}


async def print_dice(message: Message, dices: list[int]) -> None:
    result = ''.join([DICES[dice] for dice in dices])
    await message.answer(f'{result}')
