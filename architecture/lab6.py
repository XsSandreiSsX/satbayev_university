import random
from collections import OrderedDict

def simulate_cache(addresses, cache_size):
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
            cache[address] = True

    return hits, misses

def print_result(name, addresses, cache_size):
    hits, misses = simulate_cache(addresses, cache_size)
    total = len(addresses)
    print(f"{cache_size:<8} {name:<19} {hits:<8} {misses:<8} {hits / total * 100:>6.2f}%")


sequential = list(range(100)) * 5
random_access = [random.randrange(100) for _ in range(500)]

print("1. ОСНОВНОЙ ЭКСПЕРИМЕНТ (500 обращений)")
print(f"{'Кэш':<8} {'Тип доступа':<19} {'Hit':<8} {'Miss':<8} {'Hit rate'}")
for size in [10, 25, 50, 100]:
    print_result("Последовательный", sequential, size)
    print_result("Случайный", random_access, size)

for count in [500, 1000]:
    sequential = [i % 100 for i in range(count)]
    random_access = [random.randrange(100) for _ in range(count)]

    print(f"\n2. РАЗМЕРЫ КЭША 5, 20, 40, 80 ({count} обращений)")
    print(f"{'Кэш':<8} {'Тип доступа':<19} {'Hit':<8} {'Miss':<8} {'Hit rate'}")
    for size in [5, 20, 40, 80]:
        print_result("Последовательный", sequential, size)
        print_result("Случайный", random_access, size)



