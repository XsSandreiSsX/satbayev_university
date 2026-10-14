from dataclasses import dataclass, replace
from functools import partial


@dataclass(frozen=True)
class Item:
    name: str
    price: float
    qty: int

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Цена не может быть отрицательной")


def add_item(
    cart: tuple[Item, ...],
    item: Item
) -> tuple[Item, ...]:

    for product in cart:
        if product.name == item.name:
            return tuple(
                replace(product, qty=product.qty + item.qty)
                if product.name == item.name
                else product
                for product in cart
            )

    return cart + (item,)


def remove_item(
    cart: tuple[Item, ...],
    name: str
) -> tuple[Item, ...]:

    if not any(item.name == name for item in cart):
        raise ValueError("Товар не найден")

    return tuple(
        item for item in cart
        if item.name != name
    )


def change_qty(
    cart: tuple[Item, ...],
    name: str,
    qty: int
) -> tuple[Item, ...]:

    if not any(item.name == name for item in cart):
        raise ValueError("Товар не найден")

    if qty <= 0:
        return remove_item(cart, name)

    return tuple(
        replace(item, qty=qty)
        if item.name == name
        else item
        for item in cart
    )


def apply_discount(
    cart: tuple[Item, ...],
    percent: float
) -> tuple[Item, ...]:

    if not 0 <= percent <= 100:
        raise ValueError("Скидка должна быть от 0 до 100")

    multiplier = 1 - percent / 100

    return tuple(
        replace(item, price=item.price * multiplier)
        for item in cart
    )


def total(cart: tuple[Item, ...]) -> float:
    return sum(
        item.price * item.qty
        for item in cart
    )


def apply_operations(
    cart: tuple[Item, ...],
    operations: tuple
) -> tuple[tuple[Item, ...], ...]:

    history = (cart,)
    current_cart = cart

    for operation in operations:
        current_cart = operation(current_cart)
        history += (current_cart,)

    return history


def print_history(
    history: tuple[tuple[Item, ...], ...]
) -> None:

    print(f"{'Шаг':<6} {'Корзина':<60} {'Сумма':>12}")
    print("-" * 82)

    for step, cart in enumerate(history):
        items = ", ".join(
            f"{item.name} x{item.qty}"
            for item in cart
        )

        print(
            f"{step:<6} "
            f"{items:<60} "
            f"{total(cart):>12.0f}"
        )


if __name__ == "__main__":
    initial_cart = (
        Item("Ноутбук", 350_000, 1),
        Item("Мышь", 8_000, 2),
        Item("Клавиатура", 15_000, 1),
    )

    operations = (
        partial(
            add_item,
            item=Item("Наушники", 25_000, 1)
        ),
        partial(
            remove_item,
            name="Мышь"
        ),
        partial(
            change_qty,
            name="Клавиатура",
            qty=2
        ),
        partial(
            apply_discount,
            percent=10
        ),
    )

    history = apply_operations(
        initial_cart,
        operations
    )

    print_history(history)

    assert len(history) == 5

    assert total(history[0]) == 381_000
    assert total(history[1]) == 406_000
    assert total(history[2]) == 390_000
    assert total(history[3]) == 405_000
    assert total(history[4]) == 364_500

    assert total(initial_cart) == 381_000
    assert initial_cart == (
        Item("Ноутбук", 350_000, 1),
        Item("Мышь", 8_000, 2),
        Item("Клавиатура", 15_000, 1),
    )

    test_cart = add_item(
        initial_cart,
        Item("Мышь", 8_000, 1)
    )

    mice = tuple(
        item for item in test_cart
        if item.name == "Мышь"
    )

    assert len(mice) == 1
    assert mice[0].qty == 3

    for i in range(len(history) - 1):
        assert history[i] is not history[i + 1]

    try:
        apply_discount(initial_cart, 150)
        assert False
    except ValueError:
        pass

    try:
        remove_item(initial_cart, "Телефон")
        assert False
    except ValueError:
        pass

    try:
        Item("Ошибка", -1000, 1)
        assert False
    except ValueError:
        pass

