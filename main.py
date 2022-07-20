tfrom game import *
from dices import *
import os
from result_printer import *


def next_time():
  print('Далее... нажмите Enter')
  input()
  os.system('cls||clear')

print("Привет. Играем до 5-х очков. Начинаем!")
game = Game(Dice_list())
printer = Result_printer()

while not (printer.your_score == 5 or printer.comps_score == 5):
  game.play_round()
  printer.print_result(game.your_mark, game.your_summ, game.comps_mark, game.comps_summ)
  next_time()

printer.set_total_winner()
print('Выйти: нажмите Enter')
input()