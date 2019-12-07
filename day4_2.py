from typing import List
from itertools import count


def split_to_digits(num: int) -> List[int]:
    digits = []
    while num > 0:
        digits.append(num % 10)
        num //= 10
    return list(reversed(digits))



initial = 246666
final = 739105

current = initial
things = 0
while current <= final:
    digits = split_to_digits(current)
    digits[-1] += 1
    for i in range(-1, -len(digits), -1):
        if digits[i] > 9:
            digits[i-1] += 1
            for j in range(i, 0, 1):
                digits[j] = digits[i-1]

    last_d = -1
    group_length = 0
    new_things = 0
    for d in digits:
        if last_d == d:
            group_length += 1
            if group_length == 1:
                new_things += 1
            elif group_length == 2:
                new_things -= 1
        else:
            group_length = 0
        last_d = d

    if new_things > 0:
        things += 1

    current = int(''.join([str(d) for d in digits]))

print(things)
