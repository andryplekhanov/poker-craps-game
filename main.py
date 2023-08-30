from tgbot.services.dice import DiceSet
from tgbot.services.game import Game
from tgbot.services.player import Player

if __name__ == "__main__":
    you = Player(name='Andrey')
    comp = Player(name='Computer')
    dice_set = DiceSet()
    game = Game(player=you, computer=comp, dices=dice_set)
    round_counter = 1

    input('\n*** CRAPS ***\nИграем до 5 очков. Чтобы бросить кубики, нажми Enter')

    while True:
        if you.score == 5 or comp.score == 5:
            game.game_over = True
            game.set_winner()
            break
        print('-' * 40)
        print(f'РАУНД {round_counter}\nТекущий счет:\t{you.name} {you.score}:{comp.score} {comp.name}')
        print('-' * 40)
        game.play_round()
        round_counter += 1
        input('\tСледующий раунд: нажмите Enter')
        print()

    print(f'Игра закончена со счетом:\t{you.name} {you.score}:{comp.score} {comp.name}')
    input('\nEnter - выход')
