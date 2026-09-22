# Задание 1, Вариант 6
import math

a, b = 4, 6
h = 0.2

func = lambda x: (math.sin(x) - pow(x, 2)) / 15
mmin = 99999999999999
ssum = 0

x = float(a)
while x <= b:
    y = func(x)
    print(f"x: {x}, result: {round(y, 2)}")
    mmin = min(mmin, y)
    if (y < 0):
        ssum += y


    x += h
    x = round(x, 2)


print(f"Min: {mmin}, Sum: {ssum}")

# Задание 2, Вариант 6
X = list(range(9 + 1))
ans = 1

for i in range(9 + 1):
    if i % 2 != 0:
        ans *= i

print(f"Произведение: {ans}")

# Задание 3, Вариант 6
X = [4, 5, 6, 1, 3, 7]
Y = [2, 5, 7, 3, 1, 8]

mx = X[0] + Y[0]

for i in range(1, len(X)):
    mx = max(mx, X[i] + Y[i])

print(f"Max Sum: {mx}")

# Задание 4, Вариант 6
size = 4

cnt = 0
matrix = [list(range(size)) for i in range(size)]
for i in range(size):
    for j in range(size):
        if j > i and matrix[i][j] != 0:
            cnt += 1

print(f"Count: {cnt}")

# Задание 5, Вариант 6
matrix = [
    [1, -2, 3, -4, 5, -6],
    [-1, 2, -3, 4, -5, 6],
    [2, -3, 4, -5, 6, -7],
    [-2, 3, -4, 5, -6, 7],
    [3, -4, 5, -6, 7, -8]
]

for j in range(6):
    res = 0 if (j + 1) % 2 == 0 else 1

    for i in range(5):
        if (j + 1) % 2 == 0 and matrix[i][j] > 0:
            res += matrix[i][j]
        elif (j + 1) % 2 != 0 and matrix[i][j] < 0:
            res *= matrix[i][j]

    print(res)
