
# task 1
celsius = [0, 15, 22.5, -5, 30]
to_f = lambda c: c * 9 / 5 + 32
farenheit = list(map(to_f, celsius))
print(farenheit)


# task 2
words = ["Алматы", "ок", "Астана", "да", "Шымкент", "Ош"]

def good1(s: str) -> bool:
    if len(s) > 2:
        return True
    return False

good2 = lambda s: len(s) > 2
filtered_words = list(filter(good1, words))
filtered_words2 = list(filter(good2, words))
print(filtered_words)
print(f"Количество {len(filtered_words)}")
print(filtered_words2)
print(f"Количество {len(filtered_words2)}")

# task 3
products = [
    {"name": "Ноутбук", "price": 350000, "in_stock": True },
    {"name": "Мышь", "price": 8000, "in_stock": False },
    {"name": "Клавиатура", "price": 15000, "in_stock": True},
    {"name": "Монитор", "price": 120000, "in_stock": True },
    {"name": "Наушники", "price": 25000, "in_stock": False}
]

instock = sorted(list(filter(lambda x: x["in_stock"], products)), key=lambda x: x["price"])
for i in instock:
    print(i["name"], '-', i["price"])

from functools import reduce

print("Итого:", reduce(lambda a, b: a + b["price"], instock, 0))

# Task 4

def apply_n_times(func, x, n: int):
    res = x
    for _ in range(n):
        res = func(res)

    return res


print(apply_n_times(lambda x: x * 2, 1, 5))
print(apply_n_times(lambda s: s + "!", "Привет", 3))
print(apply_n_times(lambda x: x - 1, 10, 0))




# task 5
rates = {"USD": 480, "EUR": 520, "RUB": 6, "KZT": 1}

payments = [
    (100, "USD"),
    (5000, "RUB"),
    (80, "EUR"),
    (200, "USD"),
    (150000, "KZT")
]

def make_converter(rate):
    return lambda x: x*rate

converters = {
    key: make_converter(value) for key, value in rates.items()
}

payments_kzt = list(map(lambda x: converters[x[1]](x[0]), payments))
print(payments_kzt)
payments_filtered = sorted(filter(lambda x: x > 45000, payments_kzt), reverse=True)
print(list(payments_filtered))
summ = reduce(lambda a, b: a+b, payments_filtered, 0)
print(summ)