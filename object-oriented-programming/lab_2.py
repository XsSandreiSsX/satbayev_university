class Color:

    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        self.__r = r
        self.__g = g
        self.__b = b


    def set_color(self, r: int | str, g: int | None = None, b: int | None = None) -> None:
        if isinstance(r, str):
            r, g, b = map(int, r.split(", "))

        for c in (r, g, b):
            if not c:
                continue

            if c < 0 or c > 255:
                raise ValueError("value must be between 0 and 255")

        if r is not None:
            self.__r = r
        if g is not None:
            self.__g = g
        if b is not None:
            self.__b = b

    def __repr__(self):
        return f"rbg({self.__r}, {self.__g}, {self.__b})"


color = Color()
print(color)

color.set_color(66, 67, 68)
print(color)

color.set_color("255, 0, 128")
print(color)

color.set_color(r=128, g=56)
print(color)
