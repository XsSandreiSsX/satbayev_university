def capitalize_words(text: str) -> str:
    return " ".join([word.capitalize() for word in text.split(" ")])

def reverse_words(word: str) -> str:
    return " ".join([word[::-1] for word in word.split(" ")])

def count_vowels(word: str) -> int:
    return sum([1 for let in word.lower() if let in "аеёиоуыэюя" + "aeiou"])

def mask_email(email: str) -> str:
    return email[0] + "*" * (len(email[:email.find("@")])-1) + email[email.find("@"):]

if __name__ == "__main__":
    s = "python"
    try:
        s[0] = "P"
    except Exception as e:
        print(e)

    print(id(s))
    s = s.capitalize()

    # ID изменится потому что мы работаем создали новый обьект строки
    print(id(s))

    text = "функции и неизменяемость в python"
    email = "student2024@university.kz"
    original_text = text

    assert capitalize_words(text) == "Функции И Неизменяемость В Python"
    assert reverse_words(text) == "иицкнуф и ьтсомеянемзиен в nohtyp"
    assert count_vowels(text) == 11
    assert mask_email(email) == "s**********@university.kz"
    assert text == original_text
