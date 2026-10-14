import datetime
import random
from unittest.mock import patch


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


if __name__ == "__main__":
    counter = 0

    assert f1(10) != f1(10)

    assert f2(3, 4) == 5

    with patch("datetime.datetime") as dt:
        dt.now.return_value.hour = 9
        first = f3(1000)

        dt.now.return_value.hour = 12
        second = f3(1000)

        assert first != second

    scores = [5, 1, 9, 3, 7]
    original = scores.copy()
    f4(scores)
    assert scores != original

    scores = [5, 1, 9, 3, 7]
    assert f4_pure(scores) == 5
    assert scores == [5, 1, 9, 3, 7]

    assert f5_pure("Алия") == 4
    print(f"Hello, {'Алия'}")

    with patch("random.choice", return_value=1):
        first = f6([1, 2, 3])

    with patch("random.choice", return_value=3):
        second = f6([1, 2, 3])

    assert first != second

    assert discount_price(1000, 9) == 1000
    assert discount_price(1000, 12) == 800.0
    assert discount_price(1000, 15) == 1000


# | Функция | Чистая? | Причина                       | Строка                  |
# |---------|---------|-------------------------------|-------------------------|
# | f1      | Нет     | изменяет глобальный counter   | counter += 1            |
# | f2      | Да      | побочных эффектов нет         | —                       |
# | f3      | Нет     | зависит от текущего времени   | datetime.datetime.now() |
# | f4      | Нет     | изменяет аргумент             | scores.sort()           |
# | f5      | Нет     | вывод в консоль               | print(...)              |
# | f6      | Нет     | случайный результат           | random.choice(items)    |