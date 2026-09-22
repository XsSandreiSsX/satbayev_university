# Задание 1
num = 10
print(bin(num)[2:])

# Задание 2
num = "101101"
print(int(num, 2))

# Задание 3
num = "11101101"
print(hex(int(num, 2))[2:])

# Задание 4
num1 = 0b101101
num2 = 0b001011

print(f"{num1 + num2:b}")

# Задание 5
print(f"{num1 - num2:b}")

# Задание 6
A = 0b10110110
B = 0b11001010
print(f"{A & B:b}")
print(f"{A | B:b}")
print(f"{A ^ B:b}")
print(f"{~A & 0xff:b}")

