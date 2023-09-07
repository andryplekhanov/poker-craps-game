from aiogram.dispatcher.filters.state import StatesGroup, State


class Games(StatesGroup):
    """
    Класс реализует состояние игры.

    Attributes:
        round_counter (int): счетчик раундов.
        last_winner (str): победитель прошлого раунда.
        trump (str): козырь для игры в Дурака.
        deck (list): колода карт.
        desk (list): карты в игре.
    """

    round_counter = State()
    last_winner = State()
    deck = State()
    desk = State()
    trump = State()


class Players(StatesGroup):
    """
    Класс реализует состояние игроков внутри игры.

    Attributes:
        player_score (int): счёт игрока
        player_dice_list (list): кубики игрока
        player_mark (int): оценка броска игрока
        player_summa (int): сумма игрока
        player_cards (list): карты игрока
        bot_cards (list): карты бота
        bot_score (int): счёт бота
        bot_dice_list (list): кубики бота
        bot_mark (int): оценка броска бота
        bot_summa (int): сумма бота
    """

    player_score = State()
    player_dice_list = State()
    player_mark = State()
    player_summa = State()
    player_cards = State()

    bot_cards = State()
    bot_score = State()
    bot_dice_list = State()
    bot_mark = State()
    bot_summa = State()


class GallowsGame(StatesGroup):
    """
    Класс реализует состояние игры Виселица.

    Attributes:
        good_letters (list): список угаданных букв.
        bad_letters (list): список ошибочных букв.
        errors (int): счетчик ошибок.
        word (list): загаданное слово в виде списка букв.
        wait_letter (str): состояние, ожидающее ввод буквы.
    """

    good_letters = State()
    bad_letters = State()
    errors = State()
    word = State()
    wait_letter = State()
