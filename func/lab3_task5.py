from copy import deepcopy


def add_bonus(salaries: dict[str, int], percent: float) -> dict[str, int]:
    for name in salaries:
        salaries[name] = int(salaries[name] * (1 + percent / 100))
    return salaries


def add_bonus_pure(salaries: dict[str, int], percent: float) -> dict[str, int]:
    return {
        name: int(value * (1 + percent / 100))
        for name, value in salaries.items()
    }


def add_skill_shallow(staff: dict, name: str, skill: str) -> dict:
    new_staff = staff.copy()
    new_staff[name]["skills"].append(skill)
    return new_staff


def add_skill_deep(staff: dict, name: str, skill: str) -> dict:
    new_staff = deepcopy(staff)
    new_staff[name]["skills"].append(skill)
    return new_staff


def add_skill_pure(staff: dict, name: str, skill: str) -> dict:
    return {
        employee: {
            "position": data["position"],
            "skills": data["skills"] + ([skill] if employee == name else [])
        }
        for employee, data in staff.items()
    }


if __name__ == "__main__":
    salaries = {
        "Алия": 300_000,
        "Ерлан": 250_000,
        "Мария": 400_000
    }

    add_bonus(salaries, 10)

    assert salaries == {
        "Алия": 330_000,
        "Ерлан": 275_000,
        "Мария": 440_000
    }

    salaries = {
        "Алия": 300_000,
        "Ерлан": 250_000,
        "Мария": 400_000
    }

    result = add_bonus_pure(salaries, 10)

    assert result == {
        "Алия": 330_000,
        "Ерлан": 275_000,
        "Мария": 440_000
    }

    assert salaries == {
        "Алия": 300_000,
        "Ерлан": 250_000,
        "Мария": 400_000
    }


    staff = {
        "Алия": {
            "position": "backend",
            "skills": ["Python", "SQL"]
        },
        "Ерлан": {
            "position": "frontend",
            "skills": ["JavaScript"]
        },
    }

    shallow = add_skill_shallow(staff, "Ерлан", "React")

    assert staff["Ерлан"]["skills"] == ["JavaScript", "React"]
    assert shallow["Ерлан"] is staff["Ерлан"]
    assert shallow["Ерлан"]["skills"] is staff["Ерлан"]["skills"]


    staff = {
        "Алия": {
            "position": "backend",
            "skills": ["Python", "SQL"]
        },
        "Ерлан": {
            "position": "frontend",
            "skills": ["JavaScript"]
        },
    }

    deep = add_skill_deep(staff, "Ерлан", "React")

    assert staff["Ерлан"]["skills"] == ["JavaScript"]
    assert deep["Ерлан"]["skills"] == ["JavaScript", "React"]

    assert deep is not staff
    assert deep["Ерлан"] is not staff["Ерлан"]
    assert deep["Ерлан"]["skills"] is not staff["Ерлан"]["skills"]


    pure = add_skill_pure(staff, "Ерлан", "React")

    assert staff["Ерлан"]["skills"] == ["JavaScript"]
    assert pure["Ерлан"]["skills"] == ["JavaScript", "React"]

    assert pure is not staff
    assert pure["Ерлан"] is not staff["Ерлан"]
    assert pure["Ерлан"]["skills"] is not staff["Ерлан"]["skills"]
