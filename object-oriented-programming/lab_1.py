class BankAccount:
    def __init__(self, account_id: int) -> None:
        self.__account_id = account_id

        self.__balance = 0

    def get_balance(self) -> int:
        return self.__balance

    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")

        self.__balance += amount

    def withdraw(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")

        if amount > self.__balance:
            raise ValueError("Недостаточный баланс для снятия")

        self.__balance -= amount

    @property
    def account_id(self) -> int:
        return self.__account_id


user1 = BankAccount(1)

print(f"Айди аккаунта: {user1.account_id}")
print(f"Текущий баланс: {user1.get_balance()}")

user1.deposit(500)
print(f"Текущий баланс: {user1.get_balance()}")

user1.withdraw(200)
print(f"Текущий баланс: {user1.get_balance()}")

try:
    user1.withdraw(-5)
except ValueError as e:
    print(e)
