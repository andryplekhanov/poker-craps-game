class Result_printer:
  def __init__(self):
    self.your_score = 0
    self.comps_score = 0

  def print_result(self, your_mark, your_summ, comps_mark, comps_summ):
    if your_mark > comps_mark:
      self.your_score += 1
      print (f'\nТы выиграл. У тебя старше комбинация.')
    elif your_mark < comps_mark:
      self.comps_score += 1
      print (f'\nКомп выиграл. У него старше комбинация.')
    else:
      if your_summ > comps_summ:
        self.your_score += 1
        print (f'\nТы выиграл. У тебя больше сумма.')
      elif your_summ < comps_summ:
        self.comps_score += 1
        print (f'\nКомп выиграл. У него больше сумма.')
      else:
        print (f'\nНичья.')
      
    print (f'Счет: {self.your_score}:{self.comps_score}')

  def set_total_winner(self):
    if self.your_score > self.comps_score:
      print ('ИТОГ: Ты выиграл со счетом ', end="")
    else:
      print ('ИТОГ: Комп выиграл со счетом ', end="")
    print (f'{self.your_score}:{self.comps_score}')