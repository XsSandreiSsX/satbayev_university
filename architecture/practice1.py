from enum import Enum


class State(Enum):
    MODIFIED = "M"
    EXCLUSIVE = "E"
    SHARED = "S"
    INVALID = "I"


class CacheLine:
    def __init__(self, address, value):
        self.address = address
        self.value = value
        self.state = State.INVALID

    def __str__(self):
        return f"Адрес: {self.address}, Значение: {self.value}, Состояние: {self.state.value}"


class Cache:
    def __init__(self, core_id):
        self.core_id = core_id
        self.lines = {}

    def read(self, address):
        if address in self.lines:
            line = self.lines[address]

            if line.state != State.INVALID:
                print(
                    f"Ядро {self.core_id}: чтение из кэша "
                    f"адреса {address}, значение = {line.value}"
                )
                return line.value

        print(f"Ядро {self.core_id}: промах кэша для адреса {address}")
        return None

    def write(self, address, value):
        if address not in self.lines:
            self.lines[address] = CacheLine(address, value)

        line = self.lines[address]
        line.value = value
        line.state = State.MODIFIED

        print(
            f"Ядро {self.core_id}: запись "
            f"{value} по адресу {address}"
        )

    def show(self):
        print(f"\nКэш ядра {self.core_id}:")

        if not self.lines:
            print("Кэш пуст")
            return

        for line in self.lines.values():
            print(line)


class Processor:
    def __init__(self):
        self.cache1 = Cache(1)
        self.cache2 = Cache(2)

    def read(self, core, address):
        cache = self.cache1 if core == 1 else self.cache2
        other_cache = self.cache2 if core == 1 else self.cache1

        value = cache.read(address)

        if value is not None:
            return value

        # Проверяем кэш второго ядра
        if address in other_cache.lines:
            other_line = other_cache.lines[address]

            if other_line.state != State.INVALID:
                value = other_line.value

                # Оба кэша теперь содержат общую копию
                other_line.state = State.SHARED
                cache.lines[address] = CacheLine(address, value)
                cache.lines[address].state = State.SHARED

                print(
                    f"Ядро {core}: данные получены "
                    f"из кэша другого ядра"
                )

                return value

        # Данные отсутствуют в обоих кэшах
        print(f"Ядро {core}: данные отсутствуют в кэшах")

        value = 0
        cache.lines[address] = CacheLine(address, value)
        cache.lines[address].state = State.EXCLUSIVE

        return value

    def write(self, core, address, value):
        cache = self.cache1 if core == 1 else self.cache2
        other_cache = self.cache2 if core == 1 else self.cache1

        # Инвалидация копии в другом кэше
        if address in other_cache.lines:
            other_cache.lines[address].state = State.INVALID

            print(
                f"Кэш ядра {other_cache.core_id}: "
                f"строка {address} переведена в состояние INVALID"
            )

        cache.write(address, value)

    def show(self):
        self.cache1.show()
        self.cache2.show()


# Демонстрация работы
processor = Processor()

print("=== Операция 1 ===")
processor.read(1, 100)

print("\n=== Операция 2 ===")
processor.read(2, 100)

print("\n=== Операция 3 ===")
processor.write(1, 100, 50)

print("\n=== Операция 4 ===")
processor.read(2, 100)

print("\n=== Итоговое состояние ===")
processor.show()
