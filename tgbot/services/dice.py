from random import randint
from typing import List


class Dice:
    def __init__(self):
        self.value = randint(1, 6)

    def __repr__(self) -> str:
        return str(self.value)

    def roll(self) -> None:
        self.value = randint(1, 6)


class DiceSet:
    def __init__(self):
        self.dice_set = [Dice() for _ in range(5)]

    def roll(self, dices=None) -> List:
        if dices:
            for dice in dices:
                dice.roll()
            return dices

        for dice in self.dice_set:
            dice.roll()
        return self.dice_set
