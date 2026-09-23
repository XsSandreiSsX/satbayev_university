commands = [
    "ADD R1, R2, R3",
    "SUB R4, R5, R6",
    "AND R7, R8, R9",
    "OR R10, R11, R12",
    "XOR R13, R14, R15",
]

stages = ["IF", "ID", "EX", "MEM", "WB"]

cycles = len(commands) + len(stages) - 1

print(f"{'Такт':<6}", end="")

for i in range(len(commands)):
    print(f"I{i + 1:<5}", end="")

print()

for cycle in range(cycles):
    print(f"{cycle + 1:<6}", end="")

    for i in range(len(commands)):
        stage = cycle - i

        if 0 <= stage < len(stages):
            print(f"{stages[stage]:<6}", end="")
        else:
            print(f"{'':<6}", end="")

    print()

without_pipeline = len(commands) * len(stages)
with_pipeline = cycles

print()
print("Без конвейера:", without_pipeline, "тактов")
print("С конвейером:", with_pipeline, "тактов")
print("Выигрыш:", without_pipeline - with_pipeline, "тактов")
print("Ускорение:", round(without_pipeline / with_pipeline, 2), "раза")