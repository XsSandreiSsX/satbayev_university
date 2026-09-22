from dataclasses import dataclass
from enum import StrEnum


class Opcode(StrEnum):
    LOAD = "LOAD"
    STORE = "STORE"
    ADD = "ADD"
    SUB = "SUB"
    CMP = "CMP"
    JMP = "JMP"
    JZ = "JZ"
    JS = "JS"
    HALT = "HALT"


@dataclass
class Instruction:
    opcode: Opcode
    args: tuple = ()

    def __str__(self):
        if not self.args:
            return self.opcode.value

        args = ", ".join(map(str, self.args))
        return f"{self.opcode.value} {args}"


class Registers:
    def __init__(self):
        self.data = {
            "R0": 0,
            "R1": 0,
            "R2": 0,
            "R3": 0,
        }

    def read(self, name):
        return self.data[name]

    def write(self, name, value):
        self.data[name] = value

    def show(self):
        print(", ".join(
            f"{name} = {value}"
            for name, value in self.data.items()
        ))


class Memory:
    def __init__(self):
        self.data = {}

    def read(self, address):
        return self.data.get(address, 0)

    def write(self, address, value):
        self.data[address] = value


@dataclass
class ExecutionResult:
    register: str | None = None
    value: int | None = None

    memory_address: int | None = None
    memory_value: int | None = None

    zf: int | None = None
    sf: int | None = None

    next_pc: int | None = None

    halt: bool = False


class CPU:
    def __init__(self):
        self.registers = Registers()
        self.memory = Memory()

        self.pc = 0

        self.ir: Instruction | None = None

        self.zf = 0
        self.sf = 0

        self.program: dict[int, Instruction] = {}

        self.running = False

    def load_program(self, program):
        self.program = program
        self.pc = 0

    def fetch(self):
        print(f"!FETCH pc: {self.pc}")

        self.ir = self.program.get(self.pc)

        if self.ir is None:
            raise RuntimeError(f"Нет команды по адресу {self.pc}")

        self.pc += 1

    def decode(self):
        opcode = self.ir.opcode
        args = self.ir.args

        print(f"!DECODE: {opcode.value} {args}")

        return opcode, args

    def execute(self, opcode, args):
        print(f"!EXECUTE")

        if opcode == Opcode.LOAD:
            register, address = args

            value = self.memory.read(address)

            return ExecutionResult(
                register=register, value=value
            )

        if opcode == Opcode.STORE:
            register, address = args

            value = self.registers.read(register)

            return ExecutionResult(
                memory_address=address,
                memory_value=value
            )

        if opcode == Opcode.ADD:
            reg1, reg2 = args

            a = self.registers.read(reg1)
            b = self.registers.read(reg2)

            result = a + b

            print(f"{a} + {b} = {result}")

            return ExecutionResult(
                register=reg1,
                value=result,

                zf=int(result == 0),
                sf=int(result < 0)
            )

        if opcode == Opcode.SUB:
            reg1, reg2 = args

            a = self.registers.read(reg1)
            b = self.registers.read(reg2)

            result = a - b

            print(f"{a} - {b} = {result}")

            return ExecutionResult(
                register=reg1,
                value=result,

                zf=int(result == 0),
                sf=int(result < 0)
            )

        if opcode == Opcode.CMP:
            reg1, reg2 = args

            a = self.registers.read(reg1)
            b = self.registers.read(reg2)

            result = a - b

            return ExecutionResult(
                zf=int(result == 0),
                sf=int(result < 0)
            )

        if opcode == Opcode.JMP:
            address = args[0]

            return ExecutionResult(
                next_pc=address,
            )

        if opcode == Opcode.JZ:
            address = args[0]

            if self.zf == 1:
                return ExecutionResult(
                    next_pc=address,
                )

            return ExecutionResult()

        if opcode == Opcode.JS:
            address = args[0]

            if self.sf == 1:
                return ExecutionResult(
                    next_pc=address,
                )

            return ExecutionResult()

        if opcode == Opcode.HALT:
            return ExecutionResult(
                halt=True,
            )
        raise ValueError("Неизвестная команда")

    def write_back(self, result: ExecutionResult):
        print("!WRITE BACK")

        if result.register is not None:
            self.registers.write(
                result.register, result.value
            )

        if result.memory_address is not None:
            self.memory.write(
                result.memory_address, result.memory_value
            )

        if result.zf is not None:
            self.zf = result.zf

        if result.sf is not None:
            self.sf = result.sf

        if result.next_pc is not None:
            self.pc = result.next_pc

        if result.halt:
            self.running = False

    def show_state(self):
        print(f"PC = {self.pc} | ", end="")
        self.registers.show()

        print(f"ZF = {self.zf}, SF = {self.sf}")
        print()

    def run(self):
        self.running = True

        while self.running:
            self.fetch()

            opcode, args = self.decode()

            result = self.execute(opcode, args)

            self.write_back(result)

            self.show_state()


ONE = 0

dumb_cpu = CPU()

dumb_cpu.memory.write(ONE, 1)

instructions = {
    0: Instruction(
        Opcode.LOAD,
        ("R0", ONE)
    ),
    1: Instruction(
        Opcode.ADD,
        ("R1", "R0")
    ),
    2: Instruction(
        Opcode.ADD,
        ("R1", "R1")
    ),
    3: Instruction(
        Opcode.ADD,
        ("R1", "R1")
    ),
    4: Instruction(
        Opcode.ADD,
        ("R1", "R1")
    ),

    5: Instruction(
        Opcode.SUB,
        ("R1", "R0")
    ),

    6: Instruction(
        Opcode.STORE,
        ("R1", 1)
    ),
    7: Instruction(
        Opcode.ADD,
        ("R2", "R0")
    ),
    8: Instruction(
        Opcode.ADD,
        ("R2", "R2")
    ),
    9: Instruction(
        Opcode.ADD,
        ("R2", "R0")
    ),
    10: Instruction(
        Opcode.ADD,
        ("R2", "R2")
    ),
    11: Instruction(
        Opcode.ADD,
        ("R2", "R2")
    ),
    12: Instruction(
        Opcode.ADD,
        ("R2", "R0")
    ),
    13: Instruction(
        Opcode.STORE,
        ("R2", 2)
    ),
    14: Instruction(
        Opcode.ADD,
        ("R3", "R2")
    ),
    15: Instruction(
        Opcode.SUB,
        ("R1", "R0")
    ),
    16: Instruction(
        Opcode.CMP,
        ("R1", "R0")
    ),
    17: Instruction(
        Opcode.JS,
        (19, )
    ),
    18: Instruction(
        Opcode.JMP,
        (14, )
    ),
    19: Instruction(
        Opcode.STORE,
        ("R3", 3)
    ),
    20: Instruction(
        Opcode.HALT
    )
}


dumb_cpu.load_program(instructions)
dumb_cpu.run()

for i in range(3 + 1):
    print(dumb_cpu.memory.read(i))

