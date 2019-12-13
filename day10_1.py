from itertools import cycle
from typing import Tuple, List
import math

Asteroid = Tuple[int, int]

asteroids: List[Asteroid] = []
with open("day10_in.txt") as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line):
            if char == "#":
                asteroids.append((x, y))


def can_see(asteroid1: Asteroid, asteroid2: Asteroid):
    if asteroid1 == asteroid2:
        return False

    dx = asteroid1[0] - asteroid2[0]
    dy = asteroid1[1] - asteroid2[1]
    gcd = math.gcd(dx, dy)
    if dx == 0:
        x_iter = cycle([asteroid1[0]])
    else:
        x_iter = range(asteroid2[0], asteroid1[0], dx // gcd)
    if dy == 0:
        y_iter = cycle([asteroid1[1]])
    else:
        y_iter = range(asteroid2[1], asteroid1[1], dy // gcd)

    for x, y in zip(x_iter, y_iter):
        if (x, y) in asteroids and (x, y) not in (asteroid1, asteroid2):
            return False
    return True


max_visible = 0
for asteroid in asteroids:
    visible = 0
    for asteroid2 in asteroids:
        if can_see(asteroid, asteroid2):
            visible += 1
    max_visible = max(max_visible, visible)

print(max_visible)
