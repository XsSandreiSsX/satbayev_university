class Song:
    def __init__(self,
                 name: str,
                 duration: int):
        self.name = name
        self.duration = duration


class Musician:
    def __init__(self, name: str):
        self.name = name


class MusicAlbum:
    def __init__(self,
                 album_name: str,
                 author: Musician,
                 songs: list[tuple[str, int]]):
        self.album_name = album_name
        self.author = author
        self.songs = [Song(name, duration) for name, duration in songs]

    def get_duration(self) -> tuple[int, int]:
        duration = 0
        for song in self.songs:
            duration += song.duration

        return duration // 60, duration % 60

    def print_info(self):
        m, s = self.get_duration()

        print(f"album: {self.album_name} • {self.author.name}")
        print(f"{m} minutes {s} seconds.\n")
        print(f"{'Song':<30}Duration")

        for song in self.songs:
            print(f"{song.name:<30}{song.duration // 60}:{song.duration % 60:02d}")


author = Musician("тёмный принц")

songs = [
    ("Welcome To Militantum", 75),
    ("завтра", 91),
    ("one more time", 110),
    ("каркоза", 100),
    ("парфюм", 97),
    ("after all", 113),
    ("одной из", 165),
    ("песня птиц", 145),
    ("предиктор", 177),
    ("хватит", 103),
    ("kiss me", 113),
    ("утекай", 100),
    ("танцуй", 116),
    ("охота на уток", 93),
    ("BURN", 162),
    ("конструктор", 100),
    ("paprika", 194),
]

album = MusicAlbum(
    album_name="MILITANTUM",
    author=author,
    songs=songs
)

album.print_info()