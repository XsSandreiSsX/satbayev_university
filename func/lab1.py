from functools import reduce
from math import pi
from typing import List

# Задание 1
circle_area = lambda r: pi * r * r
rect_perimeter = lambda a, b: (a + b) * 2
hours_to_minutes = lambda h: h * 60

print(circle_area(5))
print(rect_perimeter(4, 6))
print(hours_to_minutes(2.5))

# Задание 2
temps = [0, 20, 37, 100, -10]

celsius_to_fahrenheit = lambda lst: list(map(lambda c: (c * 1.8) + 32, lst))
print(celsius_to_fahrenheit(temps))

# Задание 3
words = ["python", "код", "функция",
         "list", "comprehension", "цикл"]

long_words = lambda lst: list(filter(lambda x: len(x) > 5, lst))
print(long_words(words))

# Задание 4

new_temps = [(i * 1.8) + 32 for i in temps]
print(new_temps == celsius_to_fahrenheit(temps))

filtered_words = [i for i in words if len(i) > 5]
print(filtered_words == long_words(words))

even_squares = [i*i for i in range(2, 20, 2)]
print(even_squares)

# Задание 5
n = 6
items = [4, 19, 2, 77, 7, 15]

max_reduce = lambda lst: reduce(lambda x, y: x if x > y else y, lst, 0)
print(max_reduce(items))

factorial_reduce = lambda n: reduce(lambda x, y: x * y, range(1, n + 1), 1)
print(factorial_reduce(n))

# Задание 6
def apply_to_all(func, items):
    return [func(item) for item in items]

items1 = [1, 2, 3, 4]
items2 = ["a", "bc", "de"]
items3 = [-2, 5, -7, 0, 3]

is_positive = lambda x: x > 0

print(apply_to_all(lambda x: x**2, items1))
print(apply_to_all(str.upper, items2))
print(apply_to_all(is_positive, items3))

# Задание 7
def count_occurrences(lst, item):
    if type(lst) != list:
        return int(lst == item)
    return sum(map(lambda x: count_occurrences(x, item), lst))

data = [1, [2, 1, [1, 3]], 1, [4, [1, 1]]]
target = 1
print(count_occurrences(data, target))

# Задание 8
employees = [
  {"name":"Айгерим","department":"IT","salary":350000},
  {"name":"Данияр","department":"Sales","salary":280000},
  {"name":"Мадина","department":"IT","salary":290000},
  {"name":"Ерлан","department":"IT","salary":410000},
]

it_high_salary_func = lambda lst: reduce(
    lambda x, y: x + y,
    map(lambda x: x["salary"],
        filter(lambda z:
               z["department"] == "IT" and z["salary"] > 300_000,
                lst)
        ), 0
)

print(it_high_salary_func(employees))

