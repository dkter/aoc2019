from dataclasses import dataclass
from enum import Enum
from itertools import zip_longest
from typing import Callable, List, Tuple


class ParamMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


def resolve(mem: List[int], val: Tuple[ParamMode, int]) -> int:
    if val[0] == ParamMode.POSITION:
        return mem[val[1]]
    else:
        return val[1]


@dataclass
class Operation:
    name: str
    opcode: int
    nargs: int
    do_thing: Callable


def _op_add(self, mem, a, b, c):
    c = c[1]
    a, b = resolve(mem, a), resolve(mem, b)
    mem[c] = a + b
    return mem, -1

def _op_mul(self, mem, a, b, c):
    c = c[1]
    a, b = resolve(mem, a), resolve(mem, b)
    mem[c] = a * b
    return mem, -1

def _op_put(self, mem, a):
    global stdin
    a = a[1]
    mem[a] = stdin.pop()
    return mem, -1

def _op_get(self, mem, a):
    a = resolve(mem, a)
    return mem, -1, a

def _op_jit(self, mem, a, b):
    a, b = resolve(mem, a), resolve(mem, b)
    ptr = -1
    if a:
        ptr = b
    return mem, ptr

def _op_jif(self, mem, a, b):
    a, b = resolve(mem, a), resolve(mem, b)
    ptr = -1
    if not a:
        ptr = b
    return mem, ptr

def _op_qlt(self, mem, a, b, c):
    a, b = resolve(mem, a), resolve(mem, b)
    c = c[1]
    if a < b:
        mem[c] = 1
    else:
        mem[c] = 0
    return mem, -1

def _op_qeq(self, mem, a, b, c):
    a, b = resolve(mem, a), resolve(mem, b)
    c = c[1]
    if a == b:
        mem[c] = 1
    else:
        mem[c] = 0
    return mem, -1

def _op_die(self, mem):
    return mem, -1


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
        return cls(op, param_modes, params[:op.nargs])


    def do_thing(self, mem):
        params = list(zip_longest(self.param_modes, self.params, fillvalue=ParamMode.POSITION))
        return self.operation.do_thing(self.operation, mem, *params)


stdin = [5]

operations = {
    1: Operation("add", 1, 3, _op_add),
    2: Operation("mul", 2, 3, _op_mul),
    3: Operation("put", 3, 1, _op_put),
    4: Operation("get", 4, 1, _op_get),
    5: Operation("jit", 5, 2, _op_jit),
    6: Operation("jif", 6, 2, _op_jif),
    7: Operation("qlt", 7, 3, _op_qlt),
    8: Operation("qeq", 8, 3, _op_qeq),
    99: Operation("die", 99, 0, _op_die),
}


with open("day5_code.txt") as f:
    code = f.read()
    mem = [int(i) for i in code.split(",")]

i = 0
op = None
while op != operations[99]:
    instr = Instruction.from_string(str(mem[i]), params=mem[i+1:])
    op = instr.operation
    print(i, op.name, instr.params, instr.param_modes, sep="\t")
    i += op.nargs + 1
    mem, ptr, *out = instr.do_thing(mem)
    if ptr != -1:
        i = ptr

    for num in out:
        print(num)
