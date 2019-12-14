class Moon:
    def __init__(self, x, y, z):
        self.dimensions = 3
        self.pos = [x, y, z]
        self.velocity = [0, 0, 0]
        self.vel_update = [0, 0, 0]


    def __imul__(self, other):
        "overloading *= for gravity bc why not"
        for index, (pos, otherpos) in enumerate(zip(self.pos, other.pos)):
            if pos < otherpos:
                self.vel_update[index] += 1
            elif otherpos < pos:
                self.vel_update[index] -= 1
        return self


    def __str__(self):
        return str(self.pos) + " " + str(self.velocity)


    def move(self):
        for i in range(self.dimensions):
            self.velocity[i] += self.vel_update[i]
            self.pos[i] += self.velocity[i]
        self.vel_update = [0, 0, 0]


moons = [
    Moon(14, 9, 14),
    Moon(9, 11, 6),
    Moon(-6, 14, -4),
    Moon(4, -4, -3)
]

for i in range(1000):
    for moon1 in moons:
        for moon2 in moons:
            # this could definitely be not O(n^2) but i'm lazy
            moon1 *= moon2
    for moon in moons:
        moon.move()

energy = 0
for moon in moons:
    pot = 0
    kin = 0
    for i in range(moon.dimensions):
        pot += abs(moon.pos[i])
        kin += abs(moon.velocity[i])
    energy += pot * kin

print(energy)
