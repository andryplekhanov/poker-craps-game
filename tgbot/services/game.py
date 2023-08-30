from collections import Counter


class Game:
    def __init__(self, player, computer, dices):
        self.player1 = player
        self.player2 = computer
        self.dices = dices
        self.winner = None
        self.game_over = False

    def play_round(self) -> None:
        if self.check_your_turn():
            self.player1.roll_dice(self.dices)
            self.ask_for_reroll()
            self.player2.roll_dice(self.dices)
            if self.should_comp_reroll():
                self.choose_dices_for_comps_reroll()
            self.set_winner()
        else:
            self.player2.roll_dice(self.dices)
            if self.should_comp_reroll():
                self.choose_dices_for_comps_reroll()
            input('\tБросить кубики: нажмите Enter')
            self.player1.roll_dice(self.dices)
            self.ask_for_reroll()
            self.set_winner()

    def ask_for_reroll(self) -> None:
        print('\tКакие кубики перебросить?\n\t\t135 - перебросить 1й, 3й и 5й кубики, а остальные '
              'оставить\n\t\t0 - не перебрасывать никакие\n\t\tEnter - перебросить все')
        reply = input('\t\t')

        if reply == '0':
            return

        reroll_nums_list = [int(num) for num in reply]  # [1, 3, 5]
        if reroll_nums_list:
            dices_for_reroll = [dice for ind, dice in enumerate(self.player1.dice_set)
                                for num in reroll_nums_list if num == ind + 1]   # ['Dice1', 'Dice3', 'Dice5']
            dices_for_save = list(set(self.player1.dice_set) - set(dices_for_reroll))  # ['Dice2', 'Dice4']
            self.player1.reroll_dice(dices=self.dices, dices_for_reroll=dices_for_reroll, dices_for_save=dices_for_save)
            return

        print('\t\tПеребросить все...', end='\t')
        self.player1.roll_dice(self.dices)

    def should_comp_reroll(self) -> bool:
        if self.winner == self.player1:
            if (self.player2.mark == self.player1.mark) and (self.player2.summa > self.player1.summa):
                print(f'\t{self.player2.name} решил не перебрасывать')
                return False
            elif self.player2.mark > self.player1.mark:
                print(f'\t{self.player2.name} решил не перебрасывать')
                return False
            return True

        if self.player2.mark >= 6:
            print(f'\t{self.player2.name} решил не перебрасывать')
            return False
        return True

    def choose_dices_for_comps_reroll(self) -> None:
        if self.player2.mark == 2:
            print(f'\t{self.player2.name} решил перебросить все...', end='\t')
            self.player2.roll_dice(self.dices)
            return

        dices_values = [dice.value for dice in self.player2.dice_set]  # [5, 4, 5, 6, 1]
        combination_dict = Counter(dices_values)  # {5: 2, 6: 1, 4: 1, 1: 1}
        dices_for_save = []

        if self.player2.mark == 3 or self.player2.mark == 4:
            for key, val in combination_dict.items():
                if val == 2:
                    for dice in self.player2.dice_set:  # ['Dice5', 'Dice4', 'Dice5', 'Dice6', 'Dice1']
                        if dice.value == key:
                            dices_for_save.append(dice)
        elif self.player2.mark == 5:
            for key, val in combination_dict.items():
                if val == 3:
                    for dice in self.player2.dice_set:  # ['Dice5', 'Dice4', 'Dice5', 'Dice6', 'Dice5']
                        if dice.value == key:
                            dices_for_save.append(dice)
        elif self.player2.mark == 9:
            for key, val in combination_dict.items():
                if val == 4:
                    for dice in self.player2.dice_set:  # ['Dice5', 'Dice5', 'Dice5', 'Dice6', 'Dice5']
                        if dice.value == key:
                            dices_for_save.append(dice)

        dices_for_reroll = list(set(self.player2.dice_set) - set(dices_for_save))
        self.player2.reroll_dice(dices=self.dices, dices_for_reroll=dices_for_reroll, dices_for_save=dices_for_save)

    def check_your_turn(self) -> bool:
        return self.winner is None or self.winner == self.player1

    def set_winner(self) -> None:
        if self.game_over:  # Если игра закончена - проверяем очки и устанавливаем победителя
            if self.player1.score > self.player2.score:
                self.winner = self.player1
            elif self.player2.score > self.player1.score:
                self.winner = self.player2
            print(f'\nПОБЕДИЛ: {self.winner.name}')
        else:  # Если игра НЕ закончена - устанавливаем победителя раунда и присваиваем очки
            if self.player1.mark > self.player2.mark:
                self.player1.score += 1
                self.winner = self.player1
                print(f'\nТы выиграл. У тебя старше комбинация.')
            elif self.player1.mark < self.player2.mark:
                self.player2.score += 1
                self.winner = self.player2
                print(f'\nКомп выиграл. У него старше комбинация.')
            else:
                if self.player1.summa > self.player2.summa:
                    self.player1.score += 1
                    self.winner = self.player1
                    print(f'\nТы выиграл. У тебя больше сумма.')
                elif self.player1.summa < self.player2.summa:
                    self.player2.score += 1
                    self.winner = self.player2
                    print(f'\nКомп выиграл. У него больше сумма.')
                else:
                    print(f'\nНичья.')
