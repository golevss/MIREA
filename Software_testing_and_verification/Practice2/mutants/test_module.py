import pytest
from module import *


def test_validate_email():
    assert validate_email("test@example.com") == True
    assert validate_email("a@b.c") == True
    assert validate_email("invalid.email") == False
    assert validate_email("user@") == False
    assert validate_email("@") == False
    assert validate_email("@a.com") == True

    assert isinstance(validate_email(123), TypeError)
    assert str(validate_email(123)) == "String value expected"
    
    assert validate_email("user@example.c om") == True
    assert validate_email("use.r@domaincom") == False
    assert validate_email("a@b@c.com") == True


def test_get_range():
    assert get_range([1, 2, 3, 4, 5]) == (1, 5)
    assert get_range([-5, 0, 5]) == (-5, 5)
    assert get_range([10]) == (10, 10)
    assert get_range((1, 3, 2)) == (1, 3)
    assert get_range({4, 2, 6}) == (2, 6)
    assert isinstance(get_range("string"), TypeError)
    assert isinstance(get_range([1, 2, "3"]), TypeError)

    assert str(get_range(123)) == "List value expected"
    assert str(get_range(["str"])) == "List must consist from integer values expected"


def test_only_even():
    assert only_even([2, 4, 6, 8]) == True
    assert only_even([0, 2, 4]) == True
    assert only_even([-2, -4, 0]) == True
    assert only_even([1, 2, 3]) == False
    assert only_even([2, 4, 5]) == False
    assert only_even([1]) == False
    assert only_even((2, 4, 6)) == True  # tuple
    assert only_even({2, 4, 8}) == True  # set

    assert isinstance(only_even("string"), TypeError)
    assert isinstance(only_even([1, "2"]), TypeError)

    assert str(only_even(123)) == "List value expected"
    assert str(only_even(["str"])) == "List must consist from integer values expected"


def test_vector_multiplier():
    assert vector_multiplier([1, 2, 3], [4, 5, 6]) == [4, 10, 18]
    assert vector_multiplier([0, 1], [2, 3]) == [0, 3]
    assert vector_multiplier([-1, 2], [3, -4]) == [-3, -8]
    assert vector_multiplier((1, 2), (3, 4)) == [3, 8]
    assert isinstance(vector_multiplier([1, 2], [1, 2, 3]), ValueError)
    assert isinstance(vector_multiplier([1, "2"], [1, 2]), TypeError)
    assert isinstance(vector_multiplier([1, 2], [1, "2"]), TypeError)

    assert str(vector_multiplier([1, 3], [4, 5, 6])) == "Vectors length must be equal"
    assert str(vector_multiplier(["str"],["str"])) == "List must consist from integer values expected"
    assert str(vector_multiplier([1, "str", 3], [4, 5, 6])) == "List must consist from integer values expected"
    assert str(vector_multiplier([1, 2, 3], [4, 5, "str"])) == "List must consist from integer values expected"

    assert isinstance(vector_multiplier([1, 2, 3], "abc"), TypeError)
    assert isinstance(vector_multiplier([1, 2, 3], "abc"), TypeError)
    assert isinstance(vector_multiplier("abc", [1, 2, 3]), TypeError)
    assert str(vector_multiplier("abc", [1, 2, 3])) == "List value expected"
    assert vector_multiplier([1, 2, 3], [4, 5, 6]) == [4, 10, 18]
    assert isinstance(vector_multiplier([1, 2], [1]), ValueError)
    

def test_upper_case():
    assert upper_case("hello") == "HELLO"
    assert upper_case("Python") == "PYTHON"
    assert upper_case("test case") == "TEST CASE"
    assert upper_case("") == ""
    assert upper_case("123abc") == "123ABC"

    assert isinstance(upper_case(123), TypeError)
    assert isinstance(upper_case([]), TypeError)

    assert str(upper_case(1)) == "String value expected"
