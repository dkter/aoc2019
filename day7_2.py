from dataclasses import dataclass
from enum import Enum
from itertools import zip_longest, permutations, cycle
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


def _op_add(self, mem, stdin, a, b, c):
    c = c[1]
    a, b = resolve(mem, a), resolve(mem, b)
    mem[c] = a + b
    return (mem, stdin), -1

def _op_mul(self, mem, stdin, a, b, c):
    c = c[1]
    a, b = resolve(mem, a), resolve(mem, b)
    mem[c] = a * b
    return (mem, stdin), -1

def _op_put(self, mem, stdin, a):
    a = a[1]
    mem[a] = stdin.pop(0)
    return (mem, stdin), -1

def _op_get(self, mem, stdin, a):
    a = resolve(mem, a)
    return (mem, stdin), -1, a

def _op_jit(self, mem, stdin, a, b):
    a, b = resolve(mem, a), resolve(mem, b)
    ptr = -1
    if a:
        ptr = b
    return (mem, stdin), ptr

def _op_jif(self, mem, stdin, a, b):
    a, b = resolve(mem, a), resolve(mem, b)
    ptr = -1
    if not a:
        ptr = b
    return (mem, stdin), ptr

def _op_qlt(self, mem, stdin, a, b, c):
    a, b = resolve(mem, a), resolve(mem, b)
    c = c[1]
    if a < b:
        mem[c] = 1
    else:
        mem[c] = 0
    return (mem, stdin), -1

def _op_qeq(self, mem, stdin, a, b, c):
    a, b = resolve(mem, a), resolve(mem, b)
    c = c[1]
    if a == b:
        mem[c] = 1
    else:
        mem[c] = 0
    return (mem, stdin), -1

def _op_die(self, mem, stdin):
    return (mem, stdin), -1


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


    def do_thing(self, mem, stdin):
        params = list(zip_longest(self.param_modes, self.params, fillvalue=ParamMode.POSITION))
        return self.operation.do_thing(self.operation, mem, stdin, *params)

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


class Amp:
    def __init__(self):
        with open("day7_code.txt") as f:
            code = f.read()
            self.mem = [int(i) for i in code.split(",")]
        self.ptr = 0

    def run(self, stdin):
        op = None
        output = []
        while op != operations[99]:
            instr = Instruction.from_string(str(self.mem[self.ptr]), params=self.mem[self.ptr+1:])
            op = instr.operation
            #print(self.ptr, op.name, stdin, instr.params, instr.param_modes, sep="\t")
            if op.name == "die":
                return None
            self.ptr += op.nargs + 1
            (self.mem, stdin), ptr, *out = instr.do_thing(self.mem, stdin)
            if ptr != -1:
                self.ptr = ptr

            if out:
                return out
        return None

max_signal = 0
done = False
for settings in permutations([5, 6, 7, 8, 9], 5):
    signal = 0
    amps = Amp(), Amp(), Amp(), Amp(), Amp()
    for setting, amp in zip_longest(settings, cycle(amps)):
        if setting is None:
            stdin = [signal]
        else:
            stdin = [setting, signal]

        output = amp.run(stdin)
        if output is None:
            break
        else:
            for o in output:
                signal = o
                max_signal = max(max_signal, o)


print(max_signal)
