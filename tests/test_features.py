"""Tests for terminal-speed features: listing, search, plain output, clipboard."""

import dorkgen.clipboard as clipboard
from dorkgen.catalog import load_catalog, search_catalog
from dorkgen.cli import EXIT_OK, main
from dorkgen.clipboard import copy_to_clipboard
from dorkgen.console_ui import format_catalog_lines


def test_search_catalog_matches_substring_case_insensitively():
    items = load_catalog(include_file_hunter=True)
    matches = search_catalog(items, "S3")
    assert matches
    assert all("s3" in item.id.lower() or "s3" in item.dork.lower() for item in matches)


def test_search_catalog_empty_term_returns_all():
    items = load_catalog(include_file_hunter=False)
    assert len(search_catalog(items, "")) == len(items)


def test_list_flag_prints_ids_and_returns_ok(capsys):
    code = main(["--list", "--no-banner"])
    assert code == EXIT_OK
    out = capsys.readouterr().out
    assert "sec.attack-surface-mapping.exposed-login-endpoints" in out


def test_search_flag_filters_output(capsys):
    code = main(["--search", "s3", "--no-banner"])
    assert code == EXIT_OK
    out = capsys.readouterr().out
    assert "amazon-s3-references" in out
    assert "admin-areas" not in out


def test_search_flag_no_match_reports_and_returns_ok(capsys):
    code = main(["--search", "zzz-nope-zzz", "--no-banner"])
    assert code == EXIT_OK
    captured = capsys.readouterr()
    assert "No catalog entries match" in captured.err


def test_plain_output_has_no_box_characters(capsys):
    code = main(["--objective", "login-portals", "--domain", "example.com", "--plain"])
    assert code == EXIT_OK
    out = capsys.readouterr().out
    assert "site:example.com" in out
    assert "+" not in out and "|" not in out and "┌" not in out


def test_format_catalog_lines_empty():
    assert format_catalog_lines([]) == []


def test_copy_to_clipboard_returns_none_without_tool(monkeypatch):
    monkeypatch.setattr(clipboard, "detect_clipboard_command", lambda: None)
    assert copy_to_clipboard("anything") is None


def test_copy_to_clipboard_uses_detected_tool(monkeypatch):
    monkeypatch.setattr(clipboard, "detect_clipboard_command", lambda: ["fake-copy"])

    captured = {}

    def fake_run(cmd, input, check, stdout, stderr):
        captured["cmd"] = cmd
        captured["input"] = input

    monkeypatch.setattr(clipboard.subprocess, "run", fake_run)
    assert copy_to_clipboard("hello") == "fake-copy"
    assert captured["cmd"] == ["fake-copy"]
    assert captured["input"] == b"hello"
