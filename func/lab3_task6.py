def register(name, group=[]):
    group.append(name)
    return group


def register_fixed(name, group=None):
    if group is None:
        group = []

    group.append(name)
    return group


def register_pure(name: str, group: tuple[str, ...] = ()) -> tuple[str, ...]:
    return group + (name,)


def get_config(key, cache={}):
    cache[key] = f"value_{key}"
    return cache


def get_config_fixed(key, cache=None):
    if cache is None:
        cache = {}

    cache[key] = f"value_{key}"
    return cache


if __name__ == "__main__":
    print(register.__defaults__)

    print(register("Алия"))
    print(register("Ерлан"))
    print(register("Мария", ["Данияр"]))
    print(register("Айгерим"))

    print(register.__defaults__)

    print(register_fixed("Алия"))
    print(register_fixed("Ерлан"))
    print(register_fixed("Мария", ["Данияр"]))
    print(register_fixed("Айгерим"))

    print(register_pure("Алия"))
    print(register_pure("Ерлан"))
    print(register_pure("Мария", ("Данияр",)))
    print(register_pure("Айгерим"))

    print(get_config("theme"))
    print(get_config("language"))

    print(get_config_fixed("theme"))
    print(get_config_fixed("language"))

