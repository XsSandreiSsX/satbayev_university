from abc import ABC, abstractmethod
from enum import StrEnum, Enum
from random import choice


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __str__(self) -> str:
        return f"{self.name}"


class Employee(Person, ABC):
    def __init__(self, name: str, age: int):
        super().__init__(name, age)
        self._workplace = None

        self._cur_order: Order | None = None

    def take_order(self, order: Order):
        self._cur_order = order

    def set_workplace(self, workplace):
        self._workplace = workplace

    @abstractmethod
    def work(self) -> None:
        ...

    @property
    def cur_order(self):
        return self._cur_order


class Cook(Employee):
    def __init__(self, name: str, age: int):
        super().__init__(name, age)

    def work(self) -> None:
        if self._cur_order is None:
            return

        if self._cur_order.status == Status.IN_KITCHEN:
            self.cur_order.set_status(Status.COOKING)

        try:
            self._workplace.use_furnace(self._cur_order.item)
        except ValueError:
            self._cur_order.edit(
                status=Status.COOKED,
                response=Response.SERVER_ERROR,
                message="Плита сломана"
            )

        self._cur_order.set_status(Status.COOKED)

        print(
            f"[COOK] {self.name} обработал "
            f"{self._cur_order.item.name} для "
            f"{self._cur_order.customer.name}"
        )

        self._cur_order = None


class Waiter(Employee):
    def __init__(self, name: str, age: int):
        super().__init__(name, age)

    def work(self) -> None:
        if self._cur_order is None:
            return

        if self._cur_order.status == Status.PENDING:
            self.cur_order.set_status(Status.TO_KITCHEN)

            print(
                f"[WAITER] {self.name}: "
                f"{self._cur_order.item.name} "
                f"для {self._cur_order.customer.name} -> кухня"
            )

            self._workplace.send_to_kitchen(self._cur_order)

        if self._cur_order.status == Status.COOKED:
            print(
                f"[WAITER] {self.name}: "
                f"{self._cur_order.item.name} "
                f"для {self._cur_order.customer.name} -> клиент"
            )

            self._cur_order.set_status(Status.READY)

            self._cur_order = None


class Customer(Person):
    def __init__(self,
                 name: str,
                 age: int
                 ):
        super().__init__(name, age)

        self.__balance = 0

    def pay(self, amount: int):
        if amount < 0:
            raise ValueError("Нельзя снять отрицательную сумму")

        if amount > self.__balance:
            raise ValueError("Недостаточно денег для списания")

        self.__balance -= amount

    def earn(self, amount: int):
        if amount < 0:
            raise ValueError("Нельзя заработать минусовую сумму")

        self.__balance += amount

    @property
    def balance(self):
        return self.__balance

    def make_order(self,
                   restaurant: Restaurant,
                   item: str):

        order = restaurant.create_order(self, item)
        return order

    def receive_order(self, order: Order) -> None:
        if order.status != Status.READY:
            raise ValueError("Заказ ещё не готов")

        try:
            self.pay(order.item.price)
        except ValueError:
            order.edit(
                status=Status.READY,
                response=Response.BAD_REQUEST,
                message="Не хватает денег получить заказ",
            )

            print(
                f"[PAYMENT][400] {self.name}: "
                f"недостаточно денег для {order.item.name}"
            )
            return

        order.edit(
            status=Status.DONE,
            response=Response.OK,
            message="Заказ успешно получен",
        )

        print(
            f"[PAYMENT][200] {self.name} получил "
            f"{order.item.name}. Баланс: {self.balance}"
        )


class MenuItem:
    def __init__(self,
                 name: str,
                 price: int,
                 difficult: int):
        self._name = name
        self._price = price
        self._difficult = difficult

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def difficult(self):
        return self._difficult


class Status(StrEnum):
    PENDING = "PENDING"
    TO_KITCHEN = "TO_KITCHEN"
    IN_KITCHEN = "IN_KITCHEN"
    COOKING = "COOKING"
    COOKED = "COOKED"
    READY = "READY"
    DONE = "DONE"


class Response(Enum):
    OK = 200
    REDIRECT = 302
    BAD_REQUEST = 400
    NOT_FOUND = 404
    FORBIDDEN = 403
    SERVER_ERROR = 500


class Order:
    def __init__(self,
                 customer: Customer,
                 item: MenuItem | None):

        self.__customer = customer
        self.__waiter: Waiter | None = None

        if not isinstance(item, MenuItem):
            self.__item = None
            self.__status = Status.DONE
            self.__response = Response.NOT_FOUND
            self.__message = "У нас нету такого блюда в меню"
        else:
            self.__item = item
            self.__status = Status.PENDING
            self.__response = None
            self.__message = None

    def set_status(self,
                   status: Status):
        self.__status = status

    def edit(self,
             status: Status,
             response: Response,
             message: str):

        self.set_status(status)

        self.__response = response
        self.__message = message

    def assign_waiter(self, waiter: Waiter) -> None:
        self.__waiter = waiter

    @property
    def customer(self):
        return self.__customer

    @property
    def waiter(self):
        return self.__waiter

    @property
    def item(self):
        return self.__item

    @property
    def status(self):
        return self.__status

    @property
    def response(self):
        return self.__response

    @property
    def message(self):
        return self.__message

    def __str__(self) -> str:
        item_name = self.__item.name if self.__item else "Не найдено"

        waiter_name = (
            self.__waiter.name
            if self.__waiter
            else "не назначен"
        )

        response = (
            f"{self.__response.name} ({self.__response.value})"
            if self.__response
            else "None"
        )

        return (
            f"Order("
            f"customer='{self.__customer.name}', "
            f"item='{item_name}', "
            f"waiter='{waiter_name}', "
            f"status={self.__status.value}, "
            f"response={response}, "
            f"message={self.__message!r}"
            f")"
        )


class Furnace:
    def __init__(self, health: int):
        self.__health = health

    @property
    def health(self):
        return self.__health

    def use(self, difficulty: int):
        self.__health = max(0, self.__health - difficulty)


class Kitchen:
    def __init__(self,
                 furnaces: list[Furnace]):

        if not furnaces:
            raise ValueError("Кухня не может работать без хотябы одной печи")

        for furnace in furnaces:
            if not isinstance(furnace, Furnace):
                raise ValueError("Переданный обьект не является плитой")

        self.__cooks: list[Cook] = []
        self.__furnaces = furnaces
        self.__orders: list[Order] = []

    def accept_order(self, order: Order):
        self.__orders.append(order)
        order.set_status(Status.IN_KITCHEN)

        print(
            f"[KITCHEN] Принят заказ {order.item.name} "
            f"для {order.customer.name} -> {order.status}"
        )

    def add_cook(self, cook: Cook):
        cook.set_workplace(self)
        self.__cooks.append(cook)

        print(
            f"[KITCHEN][HIRED] Повар: {cook.name}"
        )

    def use_furnace(self, item: MenuItem):
        work_furnace = None

        for furnace in self.__furnaces:
            if furnace.health > 0:
                work_furnace = furnace

        if not work_furnace:
            raise ValueError("Плиты поломаны")

        work_furnace.use(item.difficult)

    def run(self):
        for order in self.__orders:
            if order.status != Status.IN_KITCHEN:
                continue

            free_cook = next(
                (cook for cook in self.__cooks if cook.cur_order is None),
                None
            )

            if free_cook is None:
                print(
                    f"[KITCHEN][QUEUE] Нет свободного повара для "
                    f"{order.item.name} клиента {order.customer.name}"
                )
                break

            free_cook.take_order(order)
            order.set_status(Status.COOKING)

            print(
                f"[KITCHEN] {order.item.name} "
                f"клиента {order.customer.name} -> "
                f"повар {free_cook.name}"
            )

        for cook in self.__cooks:
            cook.work()

    @property
    def orders(self):
        return self.__orders


class Restaurant:
    def __init__(self,
                 name: str,
                 kitchen: Kitchen,
                 menu: list[MenuItem]):

        self.name = name

        self.__kitchen = kitchen
        self.__waiters: list[Waiter] = []
        self.__menu = menu

        self.__orders: list[Order] = []

    def create_order(
            self,
            customer: Customer,
            name: str
    ) -> Order:

        found_item = None

        for item in self.__menu:
            if item.name == name:
                found_item = item
                break

        current_order = Order(
            customer=customer,
            item=found_item)

        self.__orders.append(current_order)

        if current_order.response == Response.NOT_FOUND:
            print(
                f"[ORDER][404] {customer.name}: "
                f"блюда «{name}» нет в меню"
            )
            return current_order

        if not self.__waiters:
            current_order.edit(
                status=Status.DONE,
                response=Response.SERVER_ERROR,
                message="В ресторане нет официантов",
            )

            print(
                "[ORDER][500] В ресторане нет официантов"
            )

            return current_order

        waiter = choice(self.__waiters)

        print(
            f"[ORDER][NEW] {customer.name}: "
            f"{current_order.item.name} -> принял {waiter.name}"
        )

        if waiter.cur_order is not None:
            current_order.edit(
                status=Status.PENDING,
                response=Response.REDIRECT,
                message=f"Официант {waiter.name} занят. Заказ будет перенаправлен"
            )

            print(
                f"[ORDER][302] {waiter.name} занят -> "
                f"заказ {customer.name} ожидает перенаправления"
            )

            return current_order

        waiter.take_order(current_order)
        current_order.assign_waiter(waiter)

        return current_order

    def send_to_kitchen(self, order: Order) -> None:
        self.__kitchen.accept_order(order)

    def add_employee(self, employee: Cook | Waiter):
        if isinstance(employee, Waiter):
            employee.set_workplace(self)
            self.__waiters.append(employee)

            print(
                f"[RESTAURANT][HIRED] Официант: {employee.name}"
            )

        if isinstance(employee, Cook):
            self.__kitchen.add_cook(employee)

    def __distribute_orders(self, redirected: bool) -> None:
        for order in self.__orders:
            if order.status != Status.PENDING:
                continue

            if redirected and order.response != Response.REDIRECT:
                continue

            if not redirected and order.response == Response.REDIRECT:
                continue

            free_waiter = next(
                (w for w in self.__waiters if w.cur_order is None),
                None
            )

            if free_waiter is None:
                print(
                    f"[ORDER][WAIT] Нет свободного официанта для "
                    f"{order.item.name} клиента {order.customer.name}"
                )
                return

            free_waiter.take_order(order)
            order.assign_waiter(free_waiter)

            if redirected:
                print(
                    f"[ORDER][REDIRECT] {order.customer.name}: "
                    f"{order.item.name} -> {free_waiter.name}"
                )
            else:
                print(
                    f"[ORDER][ASSIGN] {order.customer.name}: "
                    f"{order.item.name} -> {free_waiter.name}"
                )

    def show_orders(self) -> None:
        print("\n---------- СОСТОЯНИЕ ЗАКАЗОВ ----------")

        if not self.__orders:
            print("Заказов пока нет")
            return

        for index, order in enumerate(self.__orders, 1):
            item_name = (
                order.item.name
                if order.item
                else "Не найдено"
            )

            waiter_name = (
                order.waiter.name
                if order.waiter
                else "-"
            )

            response = (
                f"{order.response.value} {order.response.name}"
                if order.response
                else "-"
            )

            print(
                f"#{index:<2} | "
                f"{order.customer.name:<10} | "
                f"{item_name:<30} | "
                f"{order.status.value:<10} | "
                f"waiter: {waiter_name:<10} | "
                f"{response}"
            )

        print("---------------------------------------")

    def run(self):
        print(f"\nRUN ресторана `{self.name}`")

        print("\n[ДО НАЧАЛА ЦИКЛА]")
        self.show_orders()

        print("\n[1] Перенаправляем ожидающие заказы")

        self.__distribute_orders(redirected=True)

        self.show_orders()

        print("\n[2] Официанты несут заказы на кухню")

        for waiter in self.__waiters:
            waiter.work()

        self.show_orders()

        print("\n[3] Кухня работает")

        self.__kitchen.run()

        self.show_orders()

        print("\n[4] Официанты забирают приготовленные заказы")

        for waiter in self.__waiters:
            waiter.work()

        self.show_orders()

    @property
    def orders(self):
        return self.__orders



shit_furnace = Furnace(500)
expensive_furnace = Furnace(800)

kitchen = Kitchen([
    shit_furnace,
    expensive_furnace
])

available_menu = [
    MenuItem("Пицца", 2500, 50),
    MenuItem("Стейк из мраморной говядины", 7500, 300),
    MenuItem("Паста Карбонара", 3200, 120),
    MenuItem("Бургер", 2800, 90),
    MenuItem("Рамен", 3500, 140),
    MenuItem("Лосось", 6000, 180),
    MenuItem("Салат Цезарь", 1800, 20),
]

restaurant = Restaurant(
    name="FatBody Ресторан",
    kitchen=kitchen,
    menu=available_menu
)

employees = [
    Waiter("Александр", 22),
    Waiter("Дональд", 33),
    Waiter("Франклин", 67),
    Waiter("Аркадий", 41),
    Waiter("Владислав", 27),

    # СПЕЦИАЛЬНО ДЛЯ ТЕСТОВ ПРИГЛАСИЛ ЛЕГЕНДАРНОГО
    # ИНДИЙСКОГО ШЕФ-ПОВАРА!
    Cook("Рахал Мамут", 19),
    Cook("Гастритный мастер", 25),
]

for employee in employees:
    restaurant.add_employee(employee)


customers = [
    Customer("Андрей", 19),
    Customer("madk1d", 20),
    Customer("бомж", 21),
]

customers[0].earn(30000)
customers[1].earn(15000)
customers[2].earn(500)



print("\nКЛИЕНТЫ ПРИШЛИ В РЕСТОРАН")

for customer in customers:
    print(
        f"{customer.name:<10} | баланс: {customer.balance} ₸"
    )


print("\nКЛИЕНТЫ ДЕЛАЮТ ЗАКАЗЫ")


orders = [
    customers[0].make_order(restaurant, "Пицца"),
    customers[1].make_order(restaurant, "Стейк из мраморной говядины"),
    customers[2].make_order(restaurant, "Стейк из мраморной говядины"),
    customers[0].make_order(restaurant, "Рамен"),
    customers[1].make_order(restaurant, "Лосось"),
    customers[0].make_order(restaurant, "Стейк из мраморной говядины"),
    customers[1].make_order(restaurant, "Паста Карбонара"),
    customers[0].make_order(restaurant, "Стейк из мраморной говядины"),
    customers[1].make_order(restaurant, "Стейк из мраморной говядины"),
    customers[2].make_order(restaurant, "Рамен"),
    customers[0].make_order(restaurant, "Донер"),
]



print("\n")
restaurant.show_orders()

for tick in range(1, 7):
    print(f"\n\nЦИКЛ {tick}")

    restaurant.run()

    print(
        "\n[5] Клиенты пытаются забрать готовые заказы"
    )

    for order in restaurant.orders:
        if order.status != Status.READY:
            continue

        if order.response == Response.SERVER_ERROR:
            print(
                f"[DELIVERY][500] {order.customer.name} "
                f"не получил {order.item.name}: {order.message}"
            )
            continue
        if order.response == Response.BAD_REQUEST:
            continue

        order.customer.receive_order(order)

    print(
        "\n[6] СОСТОЯНИЕ ВСЕХ ЗАКАЗОВ ПОСЛЕ ЦИКЛА"
    )

    restaurant.show_orders()

    print("\n[7] СОСТОЯНИЕ ПЕЧЕЙ")

    print(
        f"Дешевая печь:   health={shit_furnace.health}"
    )

    print(
        f"Дорогая печь:   health={expensive_furnace.health}"
    )


print("\n\nРЕСТОРАН ЗАКОНЧИЛ РАБОТУ")

print("\nФИНАЛЬНЫЕ ЗАКАЗЫ:")
restaurant.show_orders()


print("\nФИНАЛЬНЫЕ БАЛАНСЫ:")

for customer in customers:
    print(
        f"{customer.name:<10} | {customer.balance} ₸"
    )


print("\nФИНАЛЬНОЕ СОСТОЯНИЕ ПЕЧЕЙ:")

print(
    f"Дешевая печь: health={shit_furnace.health}"
)

print(
    f"Дорогая печь: health={expensive_furnace.health}"
)