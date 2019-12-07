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
    for d in digits:
        if last_d == d:
            things += 1
            break
        else:
            last_d = d

    current = int(''.join([str(d) for d in digits]))

print(things)
