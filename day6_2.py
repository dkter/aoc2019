from collections import deque

orbits = {}

with open("day6_in.txt") as f:
    for line in f.readlines():
        a, b = line.strip().split(")")
        if a in orbits:
            orbits[a].append(b)
        else:
            orbits[a] = [b]

        if b in orbits:
            orbits[b].append(a)
        else:
            orbits[b] = [a]

queue = deque()
queue.append((0, "YOU"))
visited = []
while queue:
    steps, item = queue.popleft()
    visited.append(item)
    if item == "SAN":
        print(steps - 2)
        break
    queue.extend((steps + 1, thing) for thing in orbits[item] if thing not in visited)
