import re
from functools import partial


def normalize(text: str) -> str:
    return text.lower()


def tokenize(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r"[^\W\d_]+", text))


def remove_stopwords(
    words: tuple[str, ...],
    stopwords: frozenset[str]
) -> tuple[str, ...]:
    return tuple(word for word in words if word not in stopwords)


def count_words(words: tuple[str, ...]) -> dict[str, int]:
    result = {}

    for word in words:
        result[word] = result.get(word, 0) + 1

    return result


def top_n(
    counts: dict[str, int],
    n: int
) -> tuple[tuple[str, int], ...]:
    items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return tuple(items[:n])


def compose(*funcs):
    def pipeline(value):
        for func in funcs:
            value = func(value)
        return value

    return pipeline


if __name__ == "__main__":
    text = """Python — это язык, в котором функции являются объектами первого класса.

Функции можно передавать в другие функции, а функции можно возвращать из функций.

Чистые функции не меняют данные: чистые функции возвращают новые данные.

Неизменяемые данные делают функции проще, а код — надёжнее."""

    STOPWORDS = frozenset({
        "в", "а", "и", "не", "это", "из", "можно", "котором"
    })

    analyze = compose(
        normalize,
        tokenize,
        partial(remove_stopwords, stopwords=STOPWORDS),
        count_words,
        partial(top_n, n=3)
    )

    assert normalize("Привет, МИР") == "привет, мир"

    assert tokenize("Привет, мир! 123") == ("Привет", "мир")

    words = tokenize(normalize(text))
    assert len(words) == 40

    filtered_words = remove_stopwords(words, STOPWORDS)
    assert len(filtered_words) == 30

    assert len(words) == 40

    counts = count_words(filtered_words)
    assert counts["функции"] == 7
    assert counts["данные"] == 3
    assert counts["чистые"] == 2

    assert top_n(
        {"python": 3, "java": 2, "cpp": 2},
        2
    ) == (
        ("python", 3),
        ("cpp", 2)
    )

    assert compose(
        normalize,
        tokenize
    )("Привет, МИР") == ("привет", "мир")

    assert analyze(text) == (
        ("функции", 7),
        ("данные", 3),
        ("чистые", 2)
    )

    assert STOPWORDS == frozenset({
        "в", "а", "и", "не", "это", "из", "можно", "котором"
    })

    assert isinstance(words, tuple)
    assert isinstance(filtered_words, tuple)
