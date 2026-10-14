from abc import ABC, abstractmethod


class TaxCalculator(ABC):
    @abstractmethod
    def calculateTax(self, income: float) -> float:
        pass


class FlatTax(TaxCalculator):
    def calculateTax(self, income: float) -> float:
        return income * 0.10


class ProgressiveTax(TaxCalculator):
    def calculateTax(self, income: float) -> float:
        if income <= 100_000:
            return income * 0.10

        return 100_000 * 0.10 + (income - 100_000) * 0.20


income = 200_000

flat = FlatTax()
progressive = ProgressiveTax()

print(f"Доход: {income:,.2f} тг")
print("-" * 40)

print("Фиксированная система налогообложения:")
print(f"Ставка налога: 10%")
print(f"Сумма налога: {flat.calculateTax(income):,.2f} тг")
print(f"Доход после налога: {income - flat.calculateTax(income):,.2f} тг")

print("-" * 40)

print("Прогрессивная система налогообложения:")
print("Ставка налога: 10% до 100 000 тг, далее 20%")
print(f"Сумма налога: {progressive.calculateTax(income):,.2f} тг")
print(f"Доход после налога: {income - progressive.calculateTax(income):,.2f} тг")