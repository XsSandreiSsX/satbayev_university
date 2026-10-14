import datetime
import random


counter = 0


def f1(x):
    global counter
    counter += 1
    return x * counter


def f2(a, b):
    return (a ** 2 + b ** 2) ** 0.5


def f3(price):
    if 10 <= datetime.datetime.now().hour < 14:
        return price * 0.8
    return price


def f4(scores):
    scores.sort()
    return scores[len(scores) // 2]


def f5(name):
    print(f"Hello, {name}")
    return len(name)


def f6(items):
    return random.choice(items)


def f1_pure(x, counter):
    counter += 1
    return x * counter, counter


def discount_price(price, now_hour):
    if 10 <= now_hour < 14:
        return price * 0.8
    return price


def f3_pure(price, now_hour):
    return discount_price(price, now_hour)


def f4_pure(scores):
    new_scores = sorted(scores)
    return new_scores[len(new_scores) // 2]


def f5_pure(name):
    return len(name)

# | Функция | Чистая? | Причина                       | Строка                  |
# |---------|---------|-------------------------------|-------------------------|
# | f1      | Нет     | изменяет глобальный counter   | counter += 1            |
# | f2      | Да      | побочных эффектов нет         | —                       |
# | f3      | Нет     | зависит от текущего времени   | datetime.datetime.now() |
# | f4      | Нет     | изменяет аргумент             | scores.sort()           |
# | f5      | Нет     | вывод в консоль               | print(...)              |
# | f6      | Нет     | случайный результат           | random.choice(items)    |