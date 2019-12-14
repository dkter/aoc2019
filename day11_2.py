from dataclasses import dataclass
from enum import Enum
from itertools import zip_longest, permutations, cycle
from typing import Callable, List, Tuple, Set


class ParamMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


@dataclass
class Operation:
    name: str
    opcode: int
    nargs: int
    do_thing: Callable


def _op_add(self, state, a, b, c):
    a, b = state.resolve(a), state.resolve(b)
    c = state.resolve(c, to_write=True)
    state.mem[c] = a + b
    return ()

def _op_mul(self, state, a, b, c):
    a, b = state.resolve(a), state.resolve(b)
    c = state.resolve(c, to_write=True)
    state.mem[c] = a * b
    return ()

def _op_put(self, state, a):
    a = state.resolve(a, to_write=True)
    state.mem[a] = state.stdin.pop(0)
    return ()

def _op_get(self, state, a):
    a = state.resolve(a)
    return (a,)

def _op_jit(self, state, a, b):
    a, b = state.resolve(a), state.resolve(b)
    if a:
        state.ptr = b
    return ()

def _op_jif(self, state, a, b):
    a, b = state.resolve(a), state.resolve(b)
    if not a:
        state.ptr = b
    return ()

def _op_qlt(self, state, a, b, c):
    a, b = state.resolve(a), state.resolve(b)
    c = state.resolve(c, to_write=True)
    if a < b:
        state.mem[c] = 1
    else:
        state.mem[c] = 0
    return ()

def _op_qeq(self, state, a, b, c):
    a, b = state.resolve(a), state.resolve(b)
    c = state.resolve(c, to_write=True)
    if a == b:
        state.mem[c] = 1
    else:
        state.mem[c] = 0
    return ()

def _op_srb(self, state, a):
    a = state.resolve(a)
    state.relative_base += a
    return ()

def _op_die(self, state):
    return ()


class Instruction:
    def __init__(self,
                 operation: Operation,
                 param_modes: List[ParamMode],
                 params: List[int]):
        self.operation = operation
        self.params = params
        self.param_modes = param_modes


    @classmethod
    def from_string(cls,
                    string: str,
                    params: List[int]):
        opcode = int(string[-2:])
        op = operations[opcode]
        param_modes = []
        for param_mode in string[-3::-1]:
            if param_mode == '0':
                param_modes.append(ParamMode.POSITION)
            elif param_mode == '1':
                param_modes.append(ParamMode.IMMEDIATE)
            elif param_mode == '2':
                param_modes.append(ParamMode.RELATIVE)
        return cls(op, param_modes, params[:op.nargs])


    def do_thing(self, state):
        params = list(zip_longest(self.param_modes, self.params, fillvalue=ParamMode.POSITION))
        return self.operation.do_thing(self.operation, state, *params)


operations = {
    1: Operation("add", 1, 3, _op_add),
    2: Operation("mul", 2, 3, _op_mul),
    3: Operation("put", 3, 1, _op_put),
    4: Operation("get", 4, 1, _op_get),
    5: Operation("jit", 5, 2, _op_jit),
    6: Operation("jif", 6, 2, _op_jif),
    7: Operation("qlt", 7, 3, _op_qlt),
    8: Operation("qeq", 8, 3, _op_qeq),
    9: Operation("srb", 9, 1, _op_srb),
    99: Operation("die", 99, 0, _op_die),
}


class Computer:
    def __init__(self, code):
        self.mem = code
        self.ptr = 0
        self.relative_base = 0


    def get_params(self):
        MAX_PARAM_LENGTH = 3  # this is bad
        return [self.mem.get(i, 0) for i in range(self.ptr + 1, self.ptr + MAX_PARAM_LENGTH + 1)]


    def resolve(self, val: Tuple[ParamMode, int], to_write=False) -> int:
        if val[0] == ParamMode.POSITION:
            if to_write:
                return val[1]
            else:
                return self.mem.get(val[1], 0)
        elif val[0] == ParamMode.IMMEDIATE:
            return val[1]
        elif val[0] == ParamMode.RELATIVE:
            if to_write:
                return self.relative_base + val[1]
            else:
                return self.mem.get(self.relative_base + val[1], 0)


    def run(self, stdin):
        op = None
        output = []
        self.stdin = stdin
        while op != operations[99]:
            instr = Instruction.from_string(
                str(self.mem.get(self.ptr, 0)),
                params=self.get_params())
            op = instr.operation
            #print(self.ptr, op.name, stdin, instr.params, instr.param_modes, sep="\t")
            if op.name == "die":
                return None
            self.ptr += op.nargs + 1
            out = instr.do_thing(self)
            if out:
                return out
        return None



def rotate(orientation: str, turn_direction: int) -> str:
    if turn_direction == 0:
        # rotate CCW
        if orientation == "U": return "L"
        if orientation == "L": return "D"
        if orientation == "D": return "R"
        if orientation == "R": return "U"
    elif turn_direction == 1:
        # rotate CW
        if orientation == "U": return "R"
        if orientation == "R": return "D"
        if orientation == "D": return "L"
        if orientation == "L": return "U"


def move(position: Tuple[int, int], direction: str) -> Tuple[int, int]:
    if direction == "U": return position[0], position[1] + 1
    if direction == "D": return position[0], position[1] - 1
    if direction == "L": return position[0] - 1, position[1]
    if direction == "R": return position[0] + 1, position[1]


white_panels: List[Tuple[int, int]] = []
painted_panels: Set[Tuple[int, int]] = set()
position = (0, 0)
direction = "U"

min_x = 0
max_x = 0
min_y = 0
max_y = 0

with open("day11_code.txt") as f:
    text = f.read()
    code = {index: int(instr) for index, instr in enumerate(text.split(","))}
computer = Computer(code)

colour = 1
done = False
while not done:
    new_colour = computer.run([colour])
    turn_direction = computer.run([])
    if colour is None or turn_direction is None:
        done = True
        break
    new_colour = new_colour[0]
    turn_direction = turn_direction[0]

    if new_colour == 1:
        white_panels.append(position)
    elif position in white_panels and new_colour == 0:
        white_panels.remove(position)
    painted_panels.add(position)
        
    direction = rotate(direction, turn_direction)
    position = move(position, direction)
    if position in white_panels:
        colour = 1
    else:
        colour = 0

    if position[0] > max_x: max_x = position[0]
    if position[0] < min_x: min_x = position[0]
    if position[1] > max_y: max_y = position[1]
    if position[1] < min_y: min_y = position[1]

for y in range(max_y, min_y - 1, -1):
    for x in range(min_x, max_x + 1):
        if (x, y) in white_panels:
            print("█", end="")
        else:
            print(" ", end="")
    print()
