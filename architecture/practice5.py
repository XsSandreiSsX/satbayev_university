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


memory = {
    100: 20
}


def create_instructions():
    return [
        Instruction(1, "LOAD", "R1", 100, latency=3),
        Instruction(2, "ADD", "R2", "R1", "R3"),
        Instruction(3, "MUL", "R4", "R5", "R6"),
        Instruction(4, "SUB", "R7", "R8", "R9"),
        Instruction(5, "ADD", "R10", "R4", "R11"),
    ]


def create_registers():
    return {
        "R1": None,
        "R2": None,
        "R3": 5,

        "R4": None,
        "R5": 3,
        "R6": 4,

        "R7": None,
        "R8": 15,
        "R9": 7,

        "R10": None,
        "R11": 2
    }


def is_ready(instruction, registers):
    if instruction.command == "LOAD":
        return True

    return (
        registers[instruction.src1] is not None
        and registers[instruction.src2] is not None
    )


def execute(instruction, registers):
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


def run(mode):
    instructions = create_instructions()
    registers = create_registers()

    executing = []
    cycle = 1
    current = 0

    while any(i.status != "DONE" for i in instructions):

        print(f"\nТакт {cycle}")

        for instruction in executing[:]:
            instruction.remaining -= 1

            print(
                "  Выполняется:",
                instruction,
                f"(осталось {instruction.remaining})"
            )

            if instruction.remaining == 0:
                execute(instruction, registers)

                instruction.status = "DONE"
                executing.remove(instruction)

                print("  Завершена:  ", instruction)

        if mode == "SEQUENTIAL":

            if not executing and current < len(instructions):

                instruction = instructions[current]

                if is_ready(instruction, registers):
                    instruction.status = "EXECUTING"
                    executing.append(instruction)

                    print("  Запущена:   ", instruction)

                    current += 1

        elif mode == "SUPERSCALAR":

            free_units = 2 - len(executing)

            while free_units > 0 and current < len(instructions):

                instruction = instructions[current]

                # Если следующая инструкция ждёт данные,
                # дальше по программе не идём
                if not is_ready(instruction, registers):
                    break

                instruction.status = "EXECUTING"
                executing.append(instruction)

                print("  Запущена:   ", instruction)

                current += 1
                free_units -= 1

        elif mode == "OOO":

            free_units = 2 - len(executing)

            for instruction in instructions:

                if free_units == 0:
                    break

                if instruction.status != "WAITING":
                    continue

                if is_ready(instruction, registers):

                    instruction.status = "EXECUTING"
                    executing.append(instruction)

                    print("  Запущена:   ", instruction)

                    free_units -= 1

        cycle += 1

    print("\nРезультат:")

    for reg, value in registers.items():
        print(f"{reg} = {value}")

    print(f"\nВсего тактов: {cycle - 1}")

    return cycle - 1


print("\n" + "=" * 60)
print("1. ПОСЛЕДОВАТЕЛЬНОЕ ВЫПОЛНЕНИЕ")
print("=" * 60)

sequential = run("SEQUENTIAL")


print("\n" + "=" * 60)
print("2. СУПЕРСКАЛЯРНОЕ ВЫПОЛНЕНИЕ")
print("=" * 60)

superscalar = run("SUPERSCALAR")


print("\n" + "=" * 60)
print("3. СУПЕРСКАЛЯРНОЕ + OoO")
print("=" * 60)

ooo = run("OOO")


print("\n" + "=" * 60)
print("СРАВНЕНИЕ")
print("=" * 60)

print("Последовательное     :", sequential, "тактов")
print("Суперскалярное       :", superscalar, "тактов")
print("Суперскалярное + OoO :", ooo, "тактов")