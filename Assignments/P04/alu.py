
def add(l, r):
    return l + r


def sub(l, r):
    return l - r


def mul(l, r):
    return l * r


def div(l, r):
    if(r != 0):
        return l / r
    else: 
        return l


class Alu(object):
    def __init__(self, registers):
        self.lhs = None
        self.rhs = None
        self.op = None
        self.registers = registers
        self.ops = {"ADD": add, "SUB": sub, "MUL": mul, "DIV": div}

    def exec(self, op):
        self.lhs = self.registers[0]
        self.rhs = self.registers[1]
        self.op = op.upper()
        ans = self.ops[self.op](self.lhs, self.rhs)
        return ans

    def __str__(self):
        return f"{self.lhs} {self.op} {self.rhs}"
