from datetime import timedelta, datetime
from time import sleep


class Deposit:
    __percent = 7
    def __init__(self, start_time):
        self._start_time = start_time

        self._balance = 0

    def show(self):
        return self._balance

    def deposit(self, amount: int):
        if amount <= 0:
            raise ValueError()

        self._balance += amount

    def withdraw(self, amount: int):
        if amount <= 0:
            raise ValueError("Нельзя снять отрицательную сумму")

        if self._balance < amount:
            raise ValueError("Не хватает баланса")

        self._balance -= amount

    def work(self):
        self._balance += self._balance // 100 * self.__percent


class DefaultDeposit(Deposit):
    def __init__(self, start_time):
        super().__init__(start_time)


class NakopitelniyDeposit(Deposit):
    __percent = 18
    __period = timedelta(seconds=5)

    def __init__(self, start_time):
        super().__init__(start_time)

    def withdraw(self, amount: int):
        if datetime.now() < self._start_time + self.__period:
            raise ValueError("Вы не можете сейчас снять сейчас деньги")

        super().withdraw(amount)

nnow = datetime.now()

deposit1 = DefaultDeposit(
    start_time=nnow
)

deposit2 = NakopitelniyDeposit(
    start_time=nnow
)

deposit1.deposit(
    6767
)

print(deposit1.show())
deposit1.withdraw(67)
print(deposit1.show())

deposit2.deposit(10000)

try:
    deposit2.withdraw(100)
except Exception as e:
    print(e)

print(deposit2.show())


sleep(5)

deposit2.work()
try:
    deposit2.withdraw(100)
except Exception as e:
    print(e)


print(deposit2.show())
try:
    deposit2.withdraw(-1000)
except Exception as e:
    print(e)
