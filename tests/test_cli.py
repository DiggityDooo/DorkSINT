"""Tests for CLI flag precedence, conflicts, and exit codes."""

from dorkgen.cli import EXIT_INTERRUPT, EXIT_OK, EXIT_USER_INPUT, main


def test_catalog_id_and_menu_conflict():
    assert main(["--catalog-id", "sec.x.y", "--menu"]) == EXIT_USER_INPUT


def test_catalog_id_and_objective_conflict():
    assert main(["--catalog-id", "sec.x.y", "--objective", "login-portals"]) == EXIT_USER_INPUT


def test_menu_and_objective_conflict():
    assert main(["--menu", "--objective", "login-portals"]) == EXIT_USER_INPUT


def test_bad_catalog_id_returns_user_input_error():
    assert main(["--catalog-id", "nonexistent.id.here"]) == EXIT_USER_INPUT


def test_invalid_domain_returns_user_input_error():
    assert main(["--objective", "login-portals", "--domain", "not a domain"]) == EXIT_USER_INPUT


def test_noninteractive_without_objective_returns_error():
    assert main([]) == EXIT_USER_INPUT


def test_valid_noninteractive_returns_ok(capsys):
    code = main(["--objective", "login-portals", "--domain", "example.com"])
    assert code == EXIT_OK
    captured = capsys.readouterr()
    assert "site:example.com" in captured.out
