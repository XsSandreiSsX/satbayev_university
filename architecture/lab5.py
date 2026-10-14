import time
import random


def sequential_access(N):
    data = list(range(N))

    start = time.perf_counter()

    total = 0
    for i in range(N):
        total += data[i]

    return time.perf_counter() - start


def step_access(N, step):
    data = list(range(N))

    start = time.perf_counter()

    total = 0
    for i in range(0, N, step):
        total += data[i]

    return time.perf_counter() - start


def random_access(N):
    data = list(range(N))

    indexes = list(range(N))
    random.shuffle(indexes)

    start = time.perf_counter()

    total = 0
    for i in indexes:
        total += data[i]

    return time.perf_counter() - start


print("=" * 60)
print("1. ПОСЛЕДОВАТЕЛЬНЫЙ ДОСТУП")
print("=" * 60)

N = 1_000_000

elapsed = sequential_access(N)

print(f"Размер массива: {N}")
print(f"Время: {elapsed:.6f} сек.")


print("\n" + "=" * 60)

steps = [1, 2, 4, 8, 16, 32, 64]

for step in steps:
    elapsed = step_access(N, step)

    print(
        f"Шаг: {step:<3} | "
        f"Время: {elapsed:.6f} сек."
    )


print("\n" + "=" * 60)

sequential_time = sequential_access(N)
random_time = random_access(N)

print(f"Последовательный: {sequential_time:.6f} сек.")
print(f"Случайный:       {random_time:.6f} сек.")


print("\n" + "=" * 60)

sizes = [
    10_000,
    100_000,
    1_000_000,
    5_000_000,
    10_000_000
]

for size in sizes:
    elapsed = sequential_access(size)

    print(
        f"Размер: {size:<10} | "
        f"Время: {elapsed:.6f} сек."
    )