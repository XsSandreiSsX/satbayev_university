# 1 Задание
numbers = [27, 54, 125, 200]

for n in numbers:
    print(n, bin(n)[2:], oct(n)[2:], hex(n)[2:].upper())

print()
# 2 Задание

numbers = ["101101", "1100110", "11110001", "100101011"]

for n in numbers:
    print(n, int(n, 2))

print()
# 3 Задание

print(bin(0b1011 + 0b1101)[2:])
print(bin(0b11100 - 0b1011)[2:])
print(bin(0b101 * 0b110)[2:])
print(bin(0b11000 // 0b100)[2:])

print()
# 4 Задание

a = 0b10101100
b = 0b11001101

print(bin(a & b)[2:].zfill(8))
print(bin(a | b)[2:].zfill(8))
print(bin(a ^ b)[2:].zfill(8))
print(bin((~a) & 0b11111111)[2:].zfill(8))

print()
# 5 Задание
n = -25

print(bin(256 + n)[2:])

print()

# 6 Задание
a = 25
b = -13

a_code = a
b_code = 2**8 + b

result = (a_code + b_code) % 2**8

print(bin(a_code)[2:])
print(bin(b_code)[2:])
print(bin(result)[2:])