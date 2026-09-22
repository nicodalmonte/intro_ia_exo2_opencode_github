"""Tests complets de toolbox.text_utils : is_palindrome et word_frequency.

Couverture des cas limites (edge cases) : chaînes vides, casse, espaces
spéciaux, ponctuation, chiffres, caractères accentués, etc.
"""

from toolbox.text_utils import is_palindrome, word_frequency


# ---------------------------------------------------------------------------
# is_palindrome — cas nominal (tests d'origine)
# ---------------------------------------------------------------------------

def test_is_palindrome_simple():
    assert is_palindrome("radar") is True


def test_is_palindrome_with_spaces():
    assert is_palindrome("un roc si biscornu") is True  # issues/001


def test_is_palindrome_false():
    assert is_palindrome("python") is False


# ---------------------------------------------------------------------------
# is_palindrome — cas limites
# ---------------------------------------------------------------------------

def test_is_palindrome_empty_string():
    # une chaîne vide est (techniquement) un palindrome
    assert is_palindrome("") is True


def test_is_palindrome_single_character():
    assert is_palindrome("a") is True


def test_is_palindrome_two_same_characters():
    assert is_palindrome("aa") is True


def test_is_palindrome_two_different_characters():
    assert is_palindrome("ab") is False


def test_is_palindrome_whitespace_only():
    # après suppression des espaces, il ne reste rien -> palindrome
    assert is_palindrome("   ") is True
    assert is_palindrome("\t\n  ") is True


def test_is_palindrome_ignores_case():
    assert is_palindrome("Radar") is True
    assert is_palindrome("RADAR") is True
    assert is_palindrome("RaDaR") is True


def test_is_palindrome_ignores_tabs_and_newlines():
    # isspace() couvre tabulations et retours à la ligne, pas seulement ' '
    assert is_palindrome("\tkayak\n") is True
    assert is_palindrome("ra  dar") is True  # espaces multiples en milieu


def test_is_palindrome_classic_english():
    assert is_palindrome("A Santa at NASA") is True


def test_is_palindrome_digits():
    assert is_palindrome("12321") is True
    assert is_palindrome("123") is False


def test_is_palindrome_with_spaces_but_not_palindrome():
    assert is_palindrome("ceci n est pas un palindrome") is False


def test_is_palindrome_returns_bool():
    # la fonction doit renvoyer un vrai booléen, pas une valeur truthy
    assert isinstance(is_palindrome("radar"), bool) is True
    assert isinstance(is_palindrome("python"), bool) is True


def test_is_palindrome_does_not_mutate_input():
    s = "un roc si biscornu"
    is_palindrome(s)
    assert s == "un roc si biscornu"  # la chaîne d'origine est intacte


# ---------------------------------------------------------------------------
# word_frequency — cas nominal
# ---------------------------------------------------------------------------

def test_word_frequency_simple():
    assert word_frequency("chat chat chien") == {"chat": 2, "chien": 1}


def test_word_frequency_case_insensitive():
    assert word_frequency("Chat CHAT chat") == {"chat": 3}


def test_word_frequency_ignores_punctuation():
    assert word_frequency("Chat, chat ! Chien.") == {"chat": 2, "chien": 1}


def test_word_frequency_empty():
    assert word_frequency("") == {}


# ---------------------------------------------------------------------------
# word_frequency — cas limites
# ---------------------------------------------------------------------------

def test_word_frequency_single_word():
    assert word_frequency("chat") == {"chat": 1}


def test_word_frequency_single_word_repeated_once():
    assert word_frequency("   chat   ") == {"chat": 1}


def test_word_frequency_only_spaces():
    assert word_frequency("     ") == {}


def test_word_frequency_only_punctuation():
    assert word_frequency("... !!! ???? ,,,") == {}


def test_word_frequency_only_punctuation_and_spaces():
    assert word_frequency("... !!!") == {}


def test_word_frequency_mixed_case_sentence():
    result = word_frequency("Le Le chat CHAT chien Chien CHIEN")
    assert result == {"le": 2, "chat": 2, "chien": 3}


def test_word_frequency_punctuation_between_words():
    assert word_frequency("chat;chien;chat") == {"chatchienchat": 1}
    # la ponctuation est supprimée (pas remplacée par un espace) :
    # "chat;chien" devient le mot unique "chatchien"


def test_word_frequency_punctuation_stands_alone_removed():
    assert word_frequency("oh ?! oui... non !") == {"oh": 1, "oui": 1, "non": 1}


def test_word_frequency_multiple_whitespace_types():
    # split() sans argument découpe aussi sur tabulations et retours ligne
    assert word_frequency("chat\tchien\noiseau  vache") == {
        "chat": 1,
        "chien": 1,
        "oiseau": 1,
        "vache": 1,
    }


def test_word_frequency_numbers_counted_as_words():
    assert word_frequency("3 fois 3") == {"3": 2, "fois": 1}


def test_word_frequency_accented_words():
    assert word_frequency("café Café CAFÉ") == {"café": 3}


def test_word_frequency_accented_punctuation_edge():
    # la ponctuation française accentuée (« » ’) n'est PAS dans string.punctuation
    # -> elle est conservée dans le mot (comportement documenté)
    assert word_frequency("« café »") == {"«": 1, "café": 1, "»": 1}


def test_word_frequency_apostrophe_removed():
    # l'apostrophe fait partie de string.punctuation -> supprimée
    assert word_frequency("l'ami l'ami") == {"lami": 2}


def test_word_frequency_returns_dict():
    assert isinstance(word_frequency("chat"), dict) is True


def test_word_frequency_counts_are_integers():
    result = word_frequency("chat chat")
    assert isinstance(result["chat"], int) is True
    assert result["chat"] == 2


def test_word_frequency_does_not_mutate_input():
    text = "Chat, chat !"
    word_frequency(text)
    assert text == "Chat, chat !"
