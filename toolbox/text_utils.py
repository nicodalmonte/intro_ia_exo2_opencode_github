def is_palindrome(s: str) -> bool:
    """Renvoie True si s est un palindrome (insensible à la casse et aux espaces)."""
    cleaned = "".join(ch for ch in s.lower() if not ch.isspace())  # casse et espaces ignorés
    return cleaned == cleaned[::-1]


def word_frequency(text: str) -> dict:
    """Renvoie {mot: nombre d'occurrences}, insensible à la casse et à la ponctuation.

    Toute ponctuation est retirée puis la chaîne est découpée sur les espaces ;
    les mots sont conservés en minuscules.
    """
    import string

    translator = str.maketrans("", "", string.punctuation)
    cleaned = text.lower().translate(translator)
    frequencies: dict = {}
    for word in cleaned.split():
        frequencies[word] = frequencies.get(word, 0) + 1
    return frequencies
