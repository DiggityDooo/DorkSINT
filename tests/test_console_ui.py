"""Tests for terminal output helpers and fallback behavior."""

from dorkgen.console_ui import _frame_lines, _supports_unicode, print_output_panel


def test_frame_lines_ascii_fallback(monkeypatch):
    monkeypatch.setattr("dorkgen.console_ui._supports_unicode", lambda: False)
    output = _frame_lines("Title", ["line one", "line two"])
    assert "+--" in output or "+-" in output
    assert "Title" in output
    assert "line one" in output


def test_frame_lines_unicode(monkeypatch):
    monkeypatch.setattr("dorkgen.console_ui._supports_unicode", lambda: True)
    output = _frame_lines("Title", ["hello"])
    assert "┌" in output
    assert "hello" in output


def test_print_output_panel_writes_to_stdout(capsys):
    print_output_panel(["site:example.com filetype:pdf"])
    captured = capsys.readouterr()
    assert "site:example.com" in captured.out
    assert "Generated dorks" in captured.out


def test_frame_lines_wraps_long_lines():
    long_line = "x" * 200
    output = _frame_lines("Test", [long_line])
    for line in output.split("\n"):
        assert len(line) <= 112  # max width 110 + 2 for border chars
