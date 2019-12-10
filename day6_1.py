from collections import deque

orbits = {}

with open("day6_in.txt") as f:
    for line in f.readlines():
        a, b = line.strip().split(")")
        if a in orbits:
            orbits[a].append(b)
        else:
            orbits[a] = [b]
        if b not in orbits:
            orbits[b] = []

n_orbits = 0
queue = deque()
queue.append((0, "COM"))
while queue:
    multiplier, item = queue.pop()
    queue.extend((multiplier + 1, thing) for thing in orbits[item])
    n_orbits += multiplier

print(n_orbits)
