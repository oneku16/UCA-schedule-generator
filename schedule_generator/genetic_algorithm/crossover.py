from copy import deepcopy
from random import random, randint

from schedule_generator.constraints import Subject, Slot, Room, Instructor


def f():
    n = randint(1, randint(2, 5))
    x = random()
    for _ in range(n):
        x **= 2
    return x if x > .5 else x ** 2


def random_crossover(
        individual1: list[tuple[Subject, Slot, Room, Instructor]],
        individual2: list[tuple[Subject, Slot, Room, Instructor]],
) -> tuple[list[tuple[Subject, Slot, Room, Instructor]], list[tuple[Subject, Slot, Room, Instructor]]]:
    ind1 = deepcopy(individual1)
    ind2 = deepcopy(individual2)
    probability: float = .5
    for i in range(len(individual1)):
        if random() < probability:
            ind1[i], ind2[i] = ind2[i], ind1[i]
        a = f()
        b = f()
        if random() > .5:
            probability += abs(a - b)
        else:
            probability -= abs(a - b)

        if not (0.0 <= probability <= 1.0):
            probability = .5

    return ind1, ind2
