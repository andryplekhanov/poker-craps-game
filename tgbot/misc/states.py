from aiogram.dispatcher.filters.state import StatesGroup, State


class CrapsGame(StatesGroup):
    """
    Класс реализует состояние игры.

    Attributes:
        round_counter (int): счетчик раундов.
        last_winner (str): победитель прошлого раунда.
    """

    round_counter = State()
    last_winner = State()


class CrapsPlayers(StatesGroup):
    """
    Класс реализует состояние игроков внутри игры.

    Attributes:
        player_score (int): счёт игрока
        player_dice_list (list): кубики игрока
        player_mark (int): оценка броска игрока
        player_summa (int): сумма игрока
        bot_score (int): счёт бота
        bot_dice_list (list): кубики бота
        bot_mark (int): оценка броска бота
        bot_summa (int): сумма бота
    """

    player_score = State()
    player_dice_list = State()
    player_mark = State()
    player_summa = State()

    bot_score = State()
    bot_dice_list = State()
    bot_mark = State()
    bot_summa = State()


class GallowsGame(StatesGroup):
    """
    Класс реализует состояние игры Виселица.

    Attributes:
        good_letters (list): счетчик раундов.
        bad_letters (list): победитель прошлого раунда.
        errors (int): победитель прошлого раунда.
        word (list): победитель прошлого раунда.
        wait_letter (str): победитель прошлого раунда.
    """

    good_letters = State()
    bad_letters = State()
    errors = State()
    word = State()
    wait_letter = State()
