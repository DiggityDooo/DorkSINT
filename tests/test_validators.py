import pytest

from dorkgen.validators import sanitize_many, split_csv, validate_domain


def test_validate_domain_accepts_normal_domain():
    assert validate_domain("https://Example.com/") == "example.com"


def test_validate_domain_rejects_bad_domain():
    with pytest.raises(ValueError):
        validate_domain("not a domain")


def test_split_csv_and_sanitize_many():
    raw = split_csv("pdf, docx, ,sql")
    assert raw == ["pdf", "docx", "sql"]
    assert sanitize_many(raw) == ["pdf", "docx", "sql"]

