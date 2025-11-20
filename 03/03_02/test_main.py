import builtins
import types
import pytest
import sys
from unittest.mock import patch, MagicMock

import main

def test_main_quit(monkeypatch):
    # Simulate user typing 'quit' immediately
    inputs = iter(["quit"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    with patch("main.client"):
        # Should print goodbye and exit loop
        main.main()

def test_main_chat(monkeypatch):
    # Simulate a user question and then 'quit'
    inputs = iter(["Bonjour", "quit"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    # Mock the OpenAI client response
    mock_response = MagicMock()
    mock_message = MagicMock()
    mock_message.content = [
        types.SimpleNamespace(type="text", text="Bonjour! Comment puis-je vous aider?")
    ]
    mock_response.choices = [types.SimpleNamespace(message=mock_message)]
    with patch("main.client.chat.completions.create", return_value=mock_response):
        main.main()

def test_start_menu_invalid(monkeypatch, capsys):
    # Simulate invalid menu choice then exit
    inputs = iter(["3", "2"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    with patch("main.main") as mock_main:
        with patch("sys.exit") as mock_exit:
            main.start()
            out = capsys.readouterr().out
            assert "Invalid choice" in out
            # Should not call main for invalid input
            mock_main.assert_not_called()
            # Should call sys.exit for choice 2
            # (but patched, so doesn't actually exit)
