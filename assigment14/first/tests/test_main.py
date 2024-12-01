import first
from first.first.main import say_hello


def test_say_hello():
    assert say_hello("World") == "Hello, World!"
    assert say_hello("Alice") == "Hello, Alice!"
