import pytest
from tokenizer import tokenize_text

@pytest.mark.parametrize("text, expected", [
    ("Hello world.", [["hello", "world"]]),
    ("Hello world. Bye now.", [["hello", "world"], ["bye", "now"]]),
    ("One! Two? Three.", [["one"], ["two"], ["three"]]),
    ("a lone word", [["a", "lone", "word"]]),
    ("  spaced   out  ", [["spaced", "out"]]),
    ("UPPER lower MiXeD.", [["upper", "lower", "mixed"]]),

    ("", []),
    ("hello ... world.", [["hello", "world"]]),
    ("!!!", []),
    ("ends. With. Dots.", [["ends"], ["with"], ["dots"]]),
])
def test_tokenize(text, expected):
    assert tokenize_text(text) == expected