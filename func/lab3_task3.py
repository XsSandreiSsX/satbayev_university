from math import sqrt


def distance(p1, p2) -> float:
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def move_point(p, dx, dy) -> tuple:
    return p[0] + dx, p[1] + dy


def midpoint(p1, p2) -> tuple:
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2


def polygon_perimeter(points: tuple[tuple[float, float], ...]) -> float:
    perimeter = 0

    for i in range(len(points)):
        perimeter += distance(points[i], points[(i + 1) % len(points)])

    return perimeter


if __name__ == "__main__":
    p = (3, 4)
    origin = (0, 0)
    triangle = ((0, 0), (3, 0), (3, 4))

    city_names = {
        (43.24, 76.89): "Алматы",
        (51.17, 71.45): "Астана",
    }

    assert distance(p, origin) == 5.0

    moved = move_point(p, 2, -1)
    assert moved == (5, 3)
    assert p == (3, 4)
    assert p is not moved

    assert midpoint((0, 0), (4, 6)) == (2.0, 3.0)

    try:
        p[0] = 10
    except TypeError as error:
        print(error)

    assert polygon_perimeter(triangle) == 12.0

    assert city_names[(43.24, 76.89)] == "Алматы"

    try:
        city_names[[43.24, 76.89]] = "Алматы"
    except TypeError as error:
        print(error)