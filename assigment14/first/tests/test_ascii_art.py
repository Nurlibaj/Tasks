import io
import sys
from first.first.ascii_art import load_ascii_art, display_text


def test_load_ascii_art():
    filename = "standard.txt"
    ascii_dict = load_ascii_art(filename)
    assert 32 in ascii_dict
    assert 33 in ascii_dict
    assert isinstance(ascii_dict[32], list)


def test_display_text():
    ascii_dict = load_ascii_art("standard.txt")
    expected_output ="""
  _         _     
|   |     |   |
|   | _ _ |   |
|     _ _     |
|   |     |   |
| _ |     | _ |
"""

    captured_output = io.StringIO()
    sys.stdout = captured_output
    display_text("H", ascii_dict)
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()
    assert output == expected_output, f"Ожидалось: {expected_output}, но было: {output}"
