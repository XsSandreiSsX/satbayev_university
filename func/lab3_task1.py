from functools import reduce


def rectangle_info(width: float, height: float) -> tuple[float, float]:
    if width <= 0 or height <= 0:
        raise ValueError()
    return width * height, 2 * (width + height)


def format_full_name(last: str, first: str, middle: str = "") -> str:
    last, first, middle = last.strip(), first.strip(), middle.strip()
    return f"{last[0].upper() + last[1:].lower()} {first[0].upper()}.{" " + middle[0].upper() + "." if middle else ""}"


def stats(*numbers) -> tuple[int, int, int]:
    return min(numbers), max(numbers), int(reduce(lambda x, y: x+y, numbers, 0) / len(numbers))

if __name__ == "__main__":
    area, perimeter = rectangle_info(5, 3)

    assert area == 15
    assert perimeter == 16

    area, perimeter = rectangle_info(width=4, height=2)

    assert area == 8
    assert perimeter == 12

    try:
        rectangle_info(0, 5)
        assert False
    except ValueError:
        pass


    name1 = format_full_name("иванов", "иван", "иванович")

    name2 = format_full_name(
        last="  ПЕТРОВ  ",
        first="  ПЁТР  ",
        middle="  ПЕТРОВИЧ  "
    )

    name3 = format_full_name("сидоров", "сидор")
    assert name1 == "Иванов И. И."
    assert name2 == "Петров П. П."
    assert name3 == "Сидоров С."


    minimum, maximum, average = stats(1, 2, 3, 4, 5)

    assert minimum == 1
    assert maximum == 5
    assert average == 3

    minimum, maximum, average = stats(10, 20)

    assert minimum == 10
    assert maximum == 20
    assert average == 15

    try:
        stats()
        assert False
    except ValueError:
        pass