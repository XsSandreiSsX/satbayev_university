import math


def long_func(a, x, y):
    first = (y + math.sqrt(x*x - y)) / (pow(math.cos(a), 2) + pow(math.e, x+y-7))
    second = (pow(math.sin(a), 2)) / (2 * x + y)
    return first + second


def another_func(x):
    if x >= 1:
        return 2 * x + math.sqrt(x)

    return (5 * (x*x) - 7) / (x*x + 2 * x + 1)

# Задание 1
print(round(long_func(math.pi, 6, 1)))

# Задание 2
nums = [-3, -2, 0, 1, 9]
for x in nums:
    print(another_func(x))

# Задание 3
words = {
    1: "Pascal",
    2: "Basic",
    3: "Delphi",
    4: "C++",
    5: "Fortran"
}

n = int(input())
print(words.get(n, "Повторите ввод"))