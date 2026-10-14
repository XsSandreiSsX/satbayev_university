def increment(n: int):
    print(n, id(n))
    n += 1
    print(n, id(n))


def add_suffix(s: str):
    print(s, id(s))
    s += "!"
    print(s, id(s))


def extend_tuple(t: tuple):
    print(t, id(t))
    t += (99,)
    print(t, id(t))


def append_item(lst: list):
    print(lst, id(lst))
    lst += [99]
    print(lst, id(lst))


def rebind_list(lst: list):
    print(lst, id(lst))
    lst = lst + [99]
    print(lst, id(lst))


if __name__ == "__main__":
    number = 10
    word = "Python"
    coords = (1, 2, 3)
    items = [1, 2, 3]
    items2 = [1, 2, 3]

    print(number, id(number))
    increment(number)
    print(number, id(number))

    print(word, id(word))
    add_suffix(word)
    print(word, id(word))

    print(coords, id(coords))
    extend_tuple(coords)
    print(coords, id(coords))

    print(items, id(items))
    append_item(items)
    print(items, id(items))

    print(items2, id(items2))
    rebind_list(items2)
    print(items2, id(items2))


# | Функция / тип      | Изменился объект? | Совпадает id? | Почему?                     |
# |--------------------|--------------------|---------------|-----------------------------|
# | increment / int    | Нет                | Нет           | int неизменяемый            |
# | add_suffix / str   | Нет                | Нет           | str неизменяемый            |
# | extend_tuple/tuple | Нет                | Нет           | tuple неизменяемый          |
# | append_item / list | Да                 | Да            | += изменяет список на месте |
# | rebind_list / list | Нет                | Нет           | + создаёт новый список      |