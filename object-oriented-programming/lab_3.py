class Building:
    def __init__(self, floors_count: int, has_helipad: bool):
        self.floors_count = floors_count
        self.has_helipad = has_helipad

        self.__emergency_lights = False

    def enable_emergency_lights(self):
        self.__emergency_lights = True



class Skycraper(Building):
    def __init__(self, floors_count: int, has_helipad: bool):
        super().__init__(floors_count, has_helipad)


build1 = Skycraper(
    floors_count=67,
    has_helipad=True)


