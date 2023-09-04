from tgbot.services.printer import SUITS, VALUES


async def create_deck() -> list[tuple]:
    return [(val, suit) for suit in SUITS for val in VALUES]
