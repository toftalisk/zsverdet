import random


def roll(n, eyes):
    return sum(random.randint(1, eyes) for _ in range(n))