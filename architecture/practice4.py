class Instruction:
    def __init__(self, number, command, dest=None, src1=None, src2=None):
        self.number = number
        self.command = command
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.status = "WAITING"

    def __str__(self):
        return f"{self.number}. {self.command} {self.dest or ''} {self.src1 or ''} {self.src2 or ''}"


instructions = [
    Instruction(1, "LOAD", "R1"),
    Instruction(2, "LOAD", "R2"),
    Instruction(3, "ADD", "R3", "R1", "R2"),
    Instruction(4, "SUB", "R4", "R5", "R6"),
    Instruction(5, "MUL", "R7", "R3", "R4"),
]


registers = {
    "R1": None,
    "R2": None,
    "R3": None,
    "R4": None,
    "R5": 5,
    "R6": 2,
    "R7": None,
}


def execute(instruction):
    if instruction.command == "LOAD":
        if instruction.number == 1:
            registers[instruction.dest] = 10
        else:
            registers[instruction.dest] = 20

    elif instruction.command == "ADD":
        registers[instruction.dest] = (
            registers[instruction.src1]
            + registers[instruction.src2]
        )

    elif instruction.command == "SUB":
        registers[instruction.dest] = (
            registers[instruction.src1]
            - registers[instruction.src2]
        )

    elif instruction.command == "MUL":
        registers[instruction.dest] = (
            registers[instruction.src1]
            * registers[instruction.src2]
        )

    instruction.status = "EXECUTED"


cycle = 1

while any(i.status == "WAITING" for i in instructions):

    print(f"\nТакт {cycle}")

    executed = 0

    for instruction in instructions:

        if instruction.status != "WAITING":
            continue

        ready = True

        for reg in [instruction.src1, instruction.src2]:
            if reg is not None and registers[reg] is None:
                ready = False

        if ready and executed < 2:
            execute(instruction)

            print("Выполнена:", instruction)

            executed += 1

    cycle += 1


print("\nИтог:")

for reg, value in registers.items():
    print(reg, "=", value)