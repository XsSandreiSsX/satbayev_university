import random
from collections import OrderedDict


def simulate_cache(memory, addresses, cache_size):
    cache = OrderedDict()
    hits = 0
    misses = 0

    for address in addresses:
        if address in cache:
            hits += 1
            cache.move_to_end(address)
        else:
            misses += 1
            if len(cache) >= cache_size:
                cache.popitem(last=False)
            cache[address] = memory[address]

    return hits, misses


memory = list(range(100))
count = 1000

repeated = [
    random.randrange(20) if random.random() < 0.8
    else random.randrange(20, 100)
    for _ in range(count)
]

random_access = [random.randrange(100) for _ in range(count)]

experiments = [
    ("Частые повторения", repeated, 10),
    ("Частые повторения", repeated, 20),
    ("Случайный доступ", random_access, 10)
]

print("ИССЛЕДОВАНИЕ ИЕРАРХИИ ПАМЯТИ")
print(f"Размер RAM: {len(memory)}")
print(f"Количество обращений: {count}\n")

print(f"{'Тип доступа':<21} {'Кэш':<7} {'Hit':<8} {'Miss':<8} {'Hit rate'}")

for name, addresses, size in experiments:
    hits, misses = simulate_cache(memory, addresses, size)
    hit_rate = hits / len(addresses) * 100

    print(f"{name:<21} {size:<7} {hits:<8} {misses:<8} {hit_rate:.2f}%")

print("\nСРАВНЕНИЕ ВРЕМЕНИ ДОСТУПА")

cache_time = 1
ram_time = 7

print(f"{'Тип доступа':<21} {'Кэш':<7} {'Без кэша':<12} {'С кэшем':<12}")

for name, addresses, size in experiments:
    hits, misses = simulate_cache(memory, addresses, size)

    without_cache = len(addresses) * ram_time
    with_cache = hits * cache_time + misses * ram_time

    print(f"{name:<21} {size:<7} {without_cache:<12} {with_cache:<12}")