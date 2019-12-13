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


def can_see(asteroid1: Asteroid, asteroid2: Asteroid) -> bool:
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


def get_angle(asteroid1: Asteroid, asteroid2: Asteroid) -> float:
    return math.atan2(asteroid1[1] - asteroid2[1],
                      asteroid2[0] - asteroid1[0])


print("Finding max visible asteroid (may take a while)...")

max_visible = 0
max_visible_asteroid: Asteroid = None
for asteroid in asteroids:
    visible = 0
    for asteroid2 in asteroids:
        if can_see(asteroid, asteroid2):
            visible += 1
    if visible > max_visible:
        max_visible = visible
        max_visible_asteroid = asteroid

print("done")
#print(max_visible_asteroid, get_angle(max_visible_asteroid, (8, 1)))

current_angle = math.pi/2-0.0001
initial = True
direction = 1
for i in range(200):
    next_asteroid: Asteroid = None
    did_something = False
    thing_works = False
    while not thing_works:
        thing_works = True
        for asteroid in asteroids:
            if next_asteroid is None:
                next_asteroid = asteroid
                continue

            asteroid_angle = get_angle(max_visible_asteroid, asteroid)
            best_angle = get_angle(max_visible_asteroid, next_asteroid)
            if (asteroid != max_visible_asteroid and
                ((initial and asteroid_angle == math.pi/2) or
                 (current_angle > asteroid_angle and abs(asteroid_angle - current_angle) < abs(best_angle - current_angle)) or
                    (asteroid_angle == best_angle and
                     math.dist(max_visible_asteroid, asteroid) < math.dist(max_visible_asteroid, next_asteroid)))):
                next_asteroid = asteroid
                did_something = True

        # check if it actually meets the criteria
        if not did_something and current_angle <= asteroid_angle:
            current_angle = math.pi+0.0001
            thing_works = False
    initial = False
    current_angle = get_angle(max_visible_asteroid, next_asteroid)
    #print(max_visible_asteroid, next_asteroid, current_angle)

    # vaporise
    asteroids.remove(next_asteroid)

print(next_asteroid[0] * 100 + next_asteroid[1])
