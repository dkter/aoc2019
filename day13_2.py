from dataclasses import dataclass
from enum import Enum
from itertools import zip_longest, permutations, cycle
from typing import Callable, List, Tuple, Set, Dict
import msvcrt


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


    def copy(self):
        return Computer(self.mem.copy())


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
            if op.name == "put" and not self.stdin:
                return output
            #print(self.ptr, op.name, stdin, instr.params, instr.param_modes, sep="\t")
            if op.name == "die":
                return output
            self.ptr += op.nargs + 1
            out = instr.do_thing(self)
            output.extend(out)
        return output


def print_screen(screen: Dict[Tuple[int, int], int],
                 width: int,
                 height: int):
    for y in range(height):
        for x in range(width):
            tile = screen.get((x, y), 0)
            if tile == 0:
                print(" ", end="")
            elif tile == 1:
                print("█", end="")
            elif tile == 2:
                print("▒", end="")
            elif tile == 3:
                print("▀", end="")
            elif tile == 4:
                print("●", end="")
            else:
                print("?", end="")
        print()



with open("day13_code.txt") as f:
    text = f.read()
    code = {index: int(instr) for index, instr in enumerate(text.split(","))}
code[0] = 2
computer = Computer(code)

joystick = 0
screen = {}
max_w = 0
max_h = 0
score = 0

mode = "auto"

while True:
    output = computer.run([joystick])
    for i in range(0, len(output), 3):
        x = output[i]
        y = output[i+1]
        tile_id = output[i+2]
        if x == -1:
            score = tile_id
        else:
            screen[x, y] = tile_id

        if x > max_w: max_w = x
        if y > max_h: max_h = y

    print("score:", score)
    print_screen(screen, max_w, max_h)


    if mode == "manual":
        # lol windows only
        key = msvcrt.getch()
        if key == b"a":
            joystick = -1
        elif key == b"s":
            joystick = 0
        elif key == b"d":
            joystick = 1
        elif key == b"q":
            break
        else:
            print(key)
    elif mode == "auto":
        # predict where the ball will go
        next_output = computer.copy().run([0])
        ball_pos = None
        paddle_pos = None
        for i in range(0, len(output), 3):
            x = output[i]
            y = output[i+1]
            tile_id = output[i+2]
            if tile_id == 4:
                ball_pos = (x, y)
            elif tile_id == 3:
                paddle_pos = (x, y)
            if ball_pos is not None and paddle_pos is not None:
                break

        if ball_pos[0] < paddle_pos[0]:
            joystick = -1
        elif ball_pos[0] > paddle_pos[0]:
            joystick = 1
        else:
            joystick = 0
