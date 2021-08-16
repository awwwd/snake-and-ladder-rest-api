import random


class Dice(object):

    @classmethod
    def roll(cls):
        return random.randint(1, 6)
