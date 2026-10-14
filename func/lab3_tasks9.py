from collections import namedtuple
from dataclasses import dataclass, replace, FrozenInstanceError


StudentNT = namedtuple("StudentNT", ["name", "group", "grades"])


@dataclass(frozen=True)
class Student:
    name: str
    group: str
    grades: tuple[int, ...]


@dataclass(frozen=True)
class StudentMutableGrades:
    name: str
    group: str
    grades: list[int]


def average(s: Student) -> float:
    return sum(s.grades) / len(s.grades)


def with_grade(s: Student, grade: int) -> Student:
    return replace(s, grades=s.grades + (grade,))


def rank(students: tuple[Student, ...]) -> tuple[Student, ...]:
    return tuple(sorted(students, key=average, reverse=True))


def filter_passed(
    students: tuple[Student, ...],
    threshold: float
) -> tuple[Student, ...]:
    return tuple(s for s in students if average(s) >= threshold)


if __name__ == "__main__":
    students_raw = (
        ("Айгерим", "ИС-31", (90, 85, 78)),
        ("Данияр", "ИС-31", (60, 72, 55)),
        ("Мария", "ИС-32", (95, 98, 100)),
        ("Ерлан", "ИС-32", (45, 50, 62)),
        ("Алия", "ИС-31", (80, 88, 91)),
    )

    student_nt = StudentNT("Айгерим", "ИС-31", (90, 85, 78))
    student = Student("Айгерим", "ИС-31", (90, 85, 78))

    try:
        student_nt.name = "Мария"
    except AttributeError as error:
        print(f"{type(error).__name__}: {error}")

    try:
        student.name = "Мария"
    except FrozenInstanceError as error:
        print(f"{type(error).__name__}: {error}")

    students = tuple(
        Student(name, group, grades)
        for name, group, grades in students_raw
    )

    assert round(average(students[0]), 2) == 84.33
    assert round(average(students[1]), 2) == 62.33
    assert round(average(students[2]), 2) == 97.67
    assert round(average(students[3]), 2) == 52.33
    assert round(average(students[4]), 2) == 86.33

    ranked = rank(students)

    assert tuple(s.name for s in ranked) == (
        "Мария",
        "Алия",
        "Айгерим",
        "Данияр",
        "Ерлан",
    )

    passed = filter_passed(students, 60)

    assert len(passed) == 4
    assert "Ерлан" not in tuple(s.name for s in passed)

    aigerim = students[0]
    updated = with_grade(aigerim, 95)

    assert updated.grades == (90, 85, 78, 95)
    assert average(updated) == 87.0
    assert aigerim.grades == (90, 85, 78)
    assert updated is not aigerim

    students_set = set(students)
    assert len(students_set) == 5

    mutable = StudentMutableGrades(
        "Айгерим",
        "ИС-31",
        [90, 85, 78]
    )

    mutable.grades.append(100)

    assert mutable.grades == [90, 85, 78, 100]

    try:
        hash(mutable)
    except TypeError as error:
        print(f"{type(error).__name__}: {error}")
