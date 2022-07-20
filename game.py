from dices import *
import random
import os
import time

class Game :
  def __init__(self, dice_list):
    self.dice_list = dice_list
    self.last_winner = 'player'
    self.your_combination = []
    self.your_mark = 0
    self.your_summ = 0
    self.comps_mark = 0
    self.comps_summ = 0
    self.comps_combination = []
    self.dices_to_summ = []

  def print_dice(self, dice_list): # принимает список с номерами и печатает каждый кубик
    for d in dice_list: 
      print(self.dice_list.print_dice(d))
      
  def set_last_winner(self): # устанавливает последнего победителя, чтобы в очередном раунде выбрать, чей ход первый.
    if self.your_mark > self.comps_mark:
      self.last_winner = 'player'
    elif self.your_mark < self.comps_mark:
      self.last_winner = 'comp'
    else:
      if self.your_summ > self.comps_summ:
        self.last_winner = 'player'
      if self.your_summ < self.comps_summ:
        self.last_winner = 'comp'

  def get_mark(self, comb1, comb2, summ): # ставит оценку для функции check_combination
    mark = 0
    if comb1 == 5:
      print(f'Покер ({summ})')
      mark = 10
    elif comb1 == 4:
      print(f'Каре ({summ})')
      mark = 9
    elif comb1 == 3 and comb2 == 2:
      print(f'Фул-хаус ({summ})')
      mark = 8
    elif comb1 == 3 and comb2 == 0:
      print(f'Сет ({summ})')
      mark = 5
    elif comb1 == 2 and comb2 == 2:
      print(f'Две пары ({summ})')
      mark = 4
    elif comb1 == 0 and comb2 == 2:
      print(f'Пара ({summ})')
      mark = 3
    elif comb1 == 66:
      print(f'Малый стрейт ({summ})')
      mark = 6
    elif comb1 == 77:
      print(f'Большой стрейт ({summ})')
      mark = 7
    else:
      print(f'Ничего ({summ})')
      mark = 2
    return mark

  def count_summ(self, element, amount):
    for x in range(amount):
      self.dices_to_summ.append(element)
    return sum(self.dices_to_summ)
    
  def check_combination(self, combination): # определяет комбинацию
    comb1 = 0
    comb2 = 0
    summ = 0
    dict = {}
    
    for i in combination: # считаем, сколько раз встретилось каждое число и добавляем в словарь
      dict[i] = combination.count(i)

    for i in dict:
      if dict[i] == 5:
        comb1 = 5
        summ = self.count_summ(i, 5)
        break
      if dict[i] == 4:
        comb1 = 4
        summ = self.count_summ(i, 4)
        break
      if dict[i] == 3:
        comb1 = 3
        summ = self.count_summ(i, 3)
        for i in dict:
          if dict[i] == 2:
            comb2 = 2
            summ = self.count_summ(i, 2)
        break
      if dict[i] == 2:
        comb2 = 2
        summ = self.count_summ(i, 2)
        dict_copy = dict
        dict_copy.pop(i)
        for i in dict_copy:
          if dict_copy[i] == 2:
            comb1 = 2
            summ = self.count_summ(i, 2)
            break
          elif dict_copy[i] == 3:
            comb1 = 3
            summ = self.count_summ(i, 3)
            break
          else:
            continue
          break
        break 
      elif dict[i] == 1:
        continue
    if comb1 == 0 and comb2 == 0:
      if sum(combination) == 15:
        comb1 = 66
        summ = 15
        self.dices_to_summ = [1, 2, 3, 4, 5]
      elif sum(combination) == 20:
        comb1 = 77
        summ = 20
        self.dices_to_summ = [2, 3, 4, 5, 6]
    
    print(f'{self.dices_to_summ}') # печатаем комбинацию
    return self.get_mark(comb1, comb2, summ) # возвращает оценку из функции get_mark
  
  def players_turn(self):
    self.dices_to_summ = [] # сбрасываем сумму комбинации на 0
    print('\nЧтобы бросить кости, нажмите Enter', end=" ")
    input()
    print('Вы бросаете...')
    time.sleep(2)
    self.dice_list.roll(5) # бросает 5 кубиков
    self.your_combination = self.dice_list.dices # получаем список выпавших номеров
    self.print_dice(self.your_combination) # печатаем кубики
    self.your_mark = self.check_combination(self.your_combination)
    self.your_summ = sum(self.dices_to_summ)
  
  def comps_turn(self):
    self.dices_to_summ = [] # сбрасываем сумму комбинации на 0
    print('\nКомпьютер бросает кости...')
    time.sleep(3)
    self.dice_list.roll(5) # бросает 5 кубиков
    self.comps_combination = self.dice_list.dices # получаем список выпавших номеров
    self.print_dice(self.comps_combination) # печатаем кубики
    self.comps_mark = self.check_combination(self.comps_combination)
    self.comps_summ = sum(self.dices_to_summ)

  def should_comp_reroll(self): # комп думает, стоит ли ему перебрасывать кубики
    if self.last_winner == 'player':
      if self.comps_mark > self.your_mark:
        print('\nКомпьютер решил не перебрасывать')
        return False
      else:
        return True
    else:
      if self.comps_mark > self.your_mark and self.comps_mark >= 6:
        print('\nКомпьютер решил не перебрасывать')
        return False
      else:
        return True
  
  def chooce_dices_for_save(self): # выбирает номера, которые НЕ нужно перебрасывать
    saved_dices = [] # сюда закинем номера, которые НЕ нужно перебрасывать
    dict = {}
    
    for i in self.comps_combination: # считаем, сколько раз встретилось каждое число и добавляем в словарь
      dict[i] = self.comps_combination.count(i)
    
    for element in dict: # комп думает, какие кубики НЕ нужно перебрасывать
      if dict[element] == 4 or dict[element] == 3:
        for x in range(dict[element]):
          saved_dices.append(element)
        break
      if dict[element] == 2:
        for x in range(2):
          saved_dices.append(element)
        
        dict_copy = dict
        dict_copy.pop(element)
        
        for i in dict_copy:
          if dict_copy[i] == 2:
            for x in range(2):
              saved_dices.append(i)
            break
          else:
            continue
          break
        break 
      elif dict[element] == 1:
        continue
    return saved_dices
    
  def comps_reroll(self):
    self.dices_to_summ = [] # сбрасываем сумму комбинации на 0
    print('\nКомпьютер перебрасывает...')
    time.sleep(3)
    
    saved_dices = self.chooce_dices_for_save() # получаем список кубиков, которые не нужно перебрасывать
    self.dice_list.roll(5-len(saved_dices)) # комп перебрасывает (5 - сохраненные кубики) кубиков
    new_dice = self.dice_list.dices # получаем список выпавших номеров
    self.comps_combination = saved_dices + new_dice # суммируем 2 списка и получаем новую комбинацию
    self.print_dice(self.comps_combination) # печатаем кубики
    self.comps_mark = self.check_combination(self.comps_combination)
    self.comps_summ = sum(self.dices_to_summ)
   
  def players_reroll(self, saved_dices):
    self.dices_to_summ = [] # сбрасываем сумму комбинации на 0
    print('\nВы перебрасываете...')
    time.sleep(3)

    self.dice_list.roll(5-len(saved_dices)) # вы перебрасываете (5 - сохраненные кубики) кубиков
    new_dice = self.dice_list.dices # получаем список выпавших номеров
    self.your_combination = saved_dices + new_dice # суммируем 2 списка и получаем новую комбинацию
    self.print_dice(self.your_combination) # печатаем кубики
    self.your_mark = self.check_combination(self.your_combination)
    self.your_summ = sum(self.dices_to_summ)
  
  def ask_for_reroll(self):
    reply = input('\nКакие кубики НЕ перебрасывать?\n\n\
135 - оставить 1й, 3й и 5й кубики, а остальные перебросить\n\
0 - не перебрасывать никакие\n\
Enter - перебросить все\n')
    if reply == '0':
      return
    
    saved_dices = [] # сюда закинем номера, которые НЕ нужно перебрасывать
    list = []
    
    for i in reply:
      list.append(int(i))
    
    for number in list: #[1,4]
      for dice in self.your_combination: #[6,5,3,6,1]
        if self.your_combination.index(dice) == number-1:
          saved_dices.append(dice)
      
    self.players_reroll(saved_dices)
  
  def play_round(self):
    self.set_last_winner()                              # узнаём последнего победителя
    
    if self.last_winner == 'player':                    # если последним победил игрок
      self.players_turn()                               # игрок бросает
      self.comps_turn()                                 # комп бросает
      self.ask_for_reroll()                             # спросить игрока перебросить
      if self.should_comp_reroll():                     # должен ли комп перебросить?
        self.comps_reroll()                             # комп перебрасывает
    else:                                               # если последним победил комп
      self.comps_turn()                                 # комп бросает
      self.players_turn()                               # игрок бросает
      if self.should_comp_reroll():                     # должен ли комп перебросить?
        self.comps_reroll()                             # комп перебрасывает
      self.ask_for_reroll()                             # спросить игрока перебросить
      