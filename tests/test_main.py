"""Tests for main.py module."""
import sys
from io import StringIO
from main import main


def test_main_prints_hello_message(capsys):
    """Test that main() prints the expected hello message."""
    main()
    captured = capsys.readouterr()
    assert "Hello from senate-insight!" in captured.out


def test_main_executes_without_error():
    """Test that main() executes without raising any exceptions."""
    try:
        main()
    except Exception as e:
        assert False, f"main() raised an exception: {e}"
