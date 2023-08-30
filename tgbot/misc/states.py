from aiogram.dispatcher.filters.state import StatesGroup, State


class Game(StatesGroup):
    """
    Класс реализует состояние игры.

    Attributes:
        round_counter (int): счетчик раундов.
    """

    round_counter = State()
    last_winner = State()


class Players(StatesGroup):
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
