class Instruction:
    def __init__(self, number, command, dest=None, src1=None, src2=None, latency=1):
        self.number = number
        self.command = command
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.latency = latency

        self.status = "WAITING"
        self.remaining = latency

    def __str__(self):
        return (
            f"{self.number}. {self.command} "
            f"{self.dest or ''} {self.src1 or ''} {self.src2 or ''}"
        )


instructions = [
    Instruction(1, "LOAD", "R1", 100, latency=3),

    Instruction(2, "ADD", "R2", "R1", "R3"),

    Instruction(3, "MUL", "R4", "R5", "R6"),
    Instruction(4, "SUB", "R7", "R8", "R9"),
]


memory = {
    100: 20
}


registers = {
    "R1": None,
    "R2": None,
    "R3": 10,
    "R4": None,
    "R5": 4,
    "R6": 5,
    "R7": None,
    "R8": 30,
    "R9": 10
}


def is_ready(instruction):
    if instruction.command == "LOAD":
        return True

    return (
        registers[instruction.src1] is not None
        and registers[instruction.src2] is not None
    )


def execute(instruction):
    if instruction.command == "LOAD":
        registers[instruction.dest] = memory[instruction.src1]

    elif instruction.command == "ADD":
        registers[instruction.dest] = (
            registers[instruction.src1]
            + registers[instruction.src2]
        )

    elif instruction.command == "MUL":
        registers[instruction.dest] = (
            registers[instruction.src1]
            * registers[instruction.src2]
        )

    elif instruction.command == "SUB":
        registers[instruction.dest] = (
            registers[instruction.src1]
            - registers[instruction.src2]
        )


executing = []
cycle = 1


while any(i.status != "DONE" for i in instructions):

    print(f"\nТакт {cycle}")

    for instruction in executing[:]:

        instruction.remaining -= 1

        print(
            "Выполняется:",
            instruction,
            f"(осталось {instruction.remaining})"
        )

        if instruction.remaining == 0:

            execute(instruction)

            instruction.status = "DONE"
            executing.remove(instruction)

            print("Завершена:", instruction)


    free_units = 2 - len(executing)

    for instruction in instructions:

        if free_units == 0:
            break

        if instruction.status != "WAITING":
            continue

        if is_ready(instruction):

            instruction.status = "EXECUTING"
            executing.append(instruction)

            print("Запущена:", instruction)

            free_units -= 1

    cycle += 1


print("\n===== Результат =====")

for reg, value in registers.items():
    print(reg, "=", value)