"""Tests complets de toolbox.convert_utils : tag_reading.

Couverture des cas limites : bornes de température, listes explicites,
indépendance entre appels, absence de fuite d'état (issues/002).
Les tests sur celsius_to_fahrenheit et moving_average ne peuvent être
écrits qu'une fois ces fonctions implémentées (NotImplementedError actuel).
"""

from toolbox.convert_utils import tag_reading


# ---------------------------------------------------------------------------
# tag_reading — cas nominal (tests d'origine)
# ---------------------------------------------------------------------------

def test_tag_reading_hot():
    assert tag_reading(30) == ["chaud"]


def test_tag_reading_cold_is_independent():
    tag_reading(30)  # premier appel, sans rapport avec le second
    assert tag_reading(10) == ["froid"]  # issues/002


# ---------------------------------------------------------------------------
# tag_reading — bornes de température
# ---------------------------------------------------------------------------

def test_tag_reading_exactly_25_is_cold():
    # la condition est strictement supérieure : 25 -> 'froid'
    assert tag_reading(25) == ["froid"]


def test_tag_reading_just_above_25_is_hot():
    assert tag_reading(25.1) == ["chaud"]


def test_tag_reading_just_below_25_is_cold():
    assert tag_reading(24.9) == ["froid"]


def test_tag_reading_zero_is_cold():
    assert tag_reading(0) == ["froid"]


def test_tag_reading_negative_is_cold():
    assert tag_reading(-10) == ["froid"]


def test_tag_reading_high_value_is_hot():
    assert tag_reading(1000) == ["chaud"]


def test_tag_reading_float_value():
    assert tag_reading(30.5) == ["chaud"]


# ---------------------------------------------------------------------------
# tag_reading — argument tags explicite
# ---------------------------------------------------------------------------

def test_tag_reading_explicit_empty_list_hot():
    assert tag_reading(30, []) == ["chaud"]


def test_tag_reading_explicit_empty_list_cold():
    assert tag_reading(10, []) == ["froid"]


def test_tag_reading_appends_to_existing_list():
    tags = ["chaud"]
    assert tag_reading(10, tags) == ["chaud", "froid"]


def test_tag_reading_returns_the_same_list_object():
    # la liste fournie est mutée et renvoyée (même objet)
    tags = []
    result = tag_reading(30, tags)
    assert result is tags
    assert tags == ["chaud"]


def test_tag_reading_explicit_list_isolated_from_other_calls():
    # une liste explicite ne doit pas polluer les appels suivants sans tags
    shared = []
    tag_reading(30, shared)
    assert shared == ["chaud"]
    assert tag_reading(10) == ["froid"]


# ---------------------------------------------------------------------------
# tag_reading — indépendance entre appels (non-régression issues/002)
# ---------------------------------------------------------------------------

def test_tag_reading_no_accumulation_over_many_calls():
    for _ in range(10):
        assert tag_reading(30) == ["chaud"]
        assert tag_reading(10) == ["froid"]


def test_tag_reading_alternating_calls():
    assert tag_reading(30) == ["chaud"]
    assert tag_reading(10) == ["froid"]
    assert tag_reading(30) == ["chaud"]
    assert tag_reading(10) == ["froid"]


def test_tag_reading_default_is_not_shared_mutable():
    # vérifie explicitement l'absence du piège de l'argument par défaut mutable
    first = tag_reading(30)
    first.append("modifié manuellement")
    assert tag_reading(10) == ["froid"]  # la modification ne fuit pas


def test_tag_reading_returns_list():
    assert isinstance(tag_reading(30), list) is True
