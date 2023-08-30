from collections import Counter
from time import sleep


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.dice_set = None
        self.mark = 0
        self.summa = 0

    def check_combination(self) -> None:
        dices_values = [dice.value for dice in self.dice_set]  # [5, 5, 5, 6, 5]
        combination_dict = Counter(dices_values)  # {5: 4, 6: 1}
        combination_dict_values = sorted(list(combination_dict.values()), reverse=True)  # [4, 1]

        print(self.dice_set)

        if combination_dict_values[0] == 5:
            self.mark = 10
            self.summa = sum(dices_values)
            print(f'\tПокер ({self.summa})')
            return
        elif combination_dict_values[0] == 4:
            self.mark = 9
            self.summa = sum([key * val for key, val in combination_dict.items() if val == 4])
            print(f'\tКаре ({self.summa})')
            return
        elif combination_dict_values[0] == 3 and combination_dict_values[1] == 2:
            self.mark = 8
            self.summa = sum([key * val for key, val in combination_dict.items() if val == 3 or val == 2])
            print(f'\tФул-хаус ({self.summa})')
            return
        elif sum(dices_values) == 20 and len(combination_dict_values) == 5:
            self.mark = 7
            self.summa = 20
            print(f'\tБольшой стрейт ({self.summa})')
            return
        elif sum(dices_values) == 15 and len(combination_dict_values) == 5:
            self.mark = 6
            self.summa = 15
            print(f'\tМалый стрейт ({self.summa})')
            return
        elif combination_dict_values[0] == 3:
            self.mark = 5
            self.summa = sum([key * val for key, val in combination_dict.items() if val == 3])
            print(f'\tСет ({self.summa})')
            return
        elif combination_dict_values[0] == 2 and combination_dict_values[1] == 2:
            self.mark = 4
            self.summa = sum([key * val for key, val in combination_dict.items() if val == 2])
            print(f'\tДве пары ({self.summa})')
            return
        elif combination_dict_values[0] == 2:
            self.mark = 3
            self.summa = sum([key * val for key, val in combination_dict.items() if val == 2])
            print(f'\tПара ({self.summa})')
            return
        else:
            self.mark = 2
            self.summa = sum(dices_values)
            print(f'\tНичего ({self.summa})')
            return

    def roll_dice(self, dices) -> None:
        print(f'\nБросает {self.name}...', end='\t')
        sleep(2)
        self.dice_set = dices.roll()
        self.check_combination()

    def reroll_dice(self, dices, dices_for_reroll, dices_for_save) -> None:
        print(f'\nПеребрасывает {self.name}...', end='\t')
        sleep(2)
        rerolled_dices = dices.roll(dices_for_reroll)
        self.dice_set = dices_for_save + rerolled_dices
        self.check_combination()
