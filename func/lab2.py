# Задание 1
import itertools
import random
import time

random.seed(100)

marks = list(random.randint(0, 100) for _ in range(20))

print(marks)
print()

filtered_marks = filter(lambda x: x >= 50, marks)
print(list(filtered_marks))

lettered_marks = list(map(lambda x: "FDCBAA"[x//20], marks))
print(lettered_marks)

print()
filtered_marks = [m for m in marks if m >= 50]

lettered_marks = ["FDCBAA"[m//20] for m in marks ]
print(filtered_marks)
print(lettered_marks)

print()

names = ["Андрей", "Мансур", "Никита", "Мамут", "Артём", "Демид"]
surnames = ["Толокань", "Саботырь", "Толеген", "Бабайкин", "Разрядный", "Зеленский"]
subnames = ["Куатулы", "Максимович", "Вадимович", "Александрович", "Американович"]

students = list(map(lambda a: " ".join(a), itertools.product(surnames, names, subnames)))
random.shuffle(students)

students = students[:15]
formatted_students = sorted(
    list(
        map(
            lambda f: f"{f.split()[0]} {f.split()[1][0]}.",
            filter(lambda x: len(x) > 3, students)
            )
        )
)

print(list(students))
print(formatted_students)

# Задание 2
import functools
summ = lambda l: functools.reduce(lambda a, b: a + b, l, 0)

mean = lambda l: summ(l) / len(l)

def dispersion(l):
    m = mean(l)
    return summ(map(lambda x: (x - m)**2, l)) / len(l)

def median(l):
    s = sorted(l)
    return (s[len(l) // 2] + s[(len(l) + 1) // 2]) / 2


compose = lambda f, g, h: lambda x: f(g(h(x)))

def pipeline(value, *funcs):
    for f in funcs:
        value = f(value)
    return value


def normalize(v):
    l = (summ(map(lambda x: x ** 2, v))) ** 0.5
    return list(map(lambda x: x / l, v))

def normalize_inplace(v):
    l = (summ(map(lambda x: x ** 2, v))) ** 0.5
    for i in range(v):
        v[i] /= l

# Задание 3
def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        stop = time.perf_counter()
        print(func.__name__, *args, kwargs)
        print(f"Время выполнения: {stop - start:5f}")

        return result

    return wrapper

@log_calls
def sample(a: int, b: int):
    return a + b

print(sample(67777777777777777, 3))
print(sample(1, 2))

print()


def validate_types(*expected_types):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(len(args)):
                if not isinstance(args[i], expected_types[i]):
                    raise TypeError(f"Значение {args[i]} не соответствует типу {expected_types[i]}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(int, int, int)
def sample_func2(a, b, c):
    return a + b // c

print(sample_func2(1, 2, 3))



def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args not in cache:
            cache[args] = func(*args)

        return cache[args]
    return wrapper

@memoize
def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)

print(fib(100))


# Задание 4

usernames = ["aigerim", "damir", "nik", "abai", "andrew", "mamut", "admin", "user1"]
actions = ["login", "logout", "message"]
statuses = ["success", "fail"]

import datetime


logs = [
    {
        "user": random.choice(usernames),
        "action": random.choice(actions),
        "status": random.choice(statuses),
        "timestamp":
            (datetime.datetime.now() +
            datetime.timedelta(
                minutes=random.randint(-10000, 10000)
            )).isoformat()

    } for i in range(30)
]

print(logs)


stmt = list(filter(
    lambda x: x["action"] == "login" and x["status"] == "fail",
    logs
))

print(stmt)

cnt = []

for user, group in itertools.groupby(sorted(stmt, key=lambda x: x["user"]), key=lambda x: x["user"]):
    cnt.append((user, len(list(group))))

print(cnt)
unique_names = sorted(list(set([e["user"] for e in logs])))
print(unique_names)


top = sorted(cnt, key=lambda x: x[1], reverse=True)[:3]
print(top)
