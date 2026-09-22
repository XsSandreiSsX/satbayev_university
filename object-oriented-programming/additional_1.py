import math
from enum import StrEnum

class LanguageEnum(StrEnum):
    RUSSIAN = "RUSSIAN"
    KAZAKH = "KAZAKH"
    ENGLISH = "ENGLISH"


def too_long_func(a: float, b: float) -> float:
    return (2.5 * math.sin(b - 2 * a) * math.exp(2 * a - b)) / math.sqrt(a**2 + b**2 - 11) + 2 * math.tan(math.pi / 4)

def calculate_y(x: float) -> float:
    if x <= 0:
        return math.sin(x**2)
    return math.cos(x**2)

def hello(language: str) -> None:
    if language == LanguageEnum.RUSSIAN:
        print("Привет")
    elif language == LanguageEnum.KAZAKH:
        print("Салем")
    elif language == LanguageEnum.ENGLISH:
        print("Hello")


# Задание 1 Вариант 4
a, b = 2, 4
print(round(too_long_func(a, b)))

# Задание 2 Вариант 4
data = [-3.14, -1.57, 0, 1.57, 5]
for x in data:
    print(round(calculate_y(x), 2))

# Задание 3 Вариант 4
available_languages = [item.value for item in LanguageEnum]
print(f"Выберите доступный язык: {", ".join(available_languages)}: ")
choice = input()
if choice not in available_languages:
    raise ValueError("Неверно указан язык")

hello(choice)


