# Класс "Кубики".
#  создать объект:  dices = Dice_list()
#  бросить кубики N раз: dices.roll(5)
#  получить список кубиков: dices.dices
#  напечатать в цикле:  print(dices.print_dice(i)) - возвращает строку
import random

class Dice_list :
  def __init__(self):
    self.dices = []

  def print_dice(self, num):
    if num == 1:
      return '┏──────┓╮\n┃   ●  ┃│\n┃      ┃│\n┗──────┛╯'
    elif num == 2:
      return '┏──────┓╮\n┃ ●    ┃│\n┃   ●  ┃│\n┗──────┛╯'
    elif num == 3:
      return '┏──────┓╮\n┃   ●  ┃│\n┃ ●  ● ┃│\n┗──────┛╯'
    elif num == 4:
      return '┏──────┓╮\n┃ ● ●  ┃│\n┃ ● ●  ┃│\n┗──────┛╯'
    elif num == 5:
      return '┏──────┓╮\n┃ ●   ●┃│\n┃ ● ● ●┃│\n┗──────┛╯'
    else:
      return '┏──────┓╮\n┃ ● ● ●┃│\n┃ ● ● ●┃│\n┗──────┛╯'

  def roll(self, amount):
    dice_list = []
    for i in range(amount):
      dice_list.append(random.randint(1, 6))
    self.dices = dice_list