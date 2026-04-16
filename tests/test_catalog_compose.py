from dorkgen.catalog import build_google_url, compose_query


def test_compose_query_prefixes_site_for_sec_mode():
    query = compose_query("inurl:admin", mode="sec", domain="example.com", keyword="")
    assert query.startswith("site:example.com ")


def test_compose_query_does_not_duplicate_site():
    query = compose_query("site:example.com inurl:login", mode="sec", domain="example.com", keyword="")
    assert query.count("site:example.com") == 1


def test_compose_query_includes_quoted_keyword():
    query = compose_query("inurl:auth", mode="sec", keyword="quarterly report")
    assert "\"quarterly report\"" in query


def test_compose_query_does_not_prepend_domain_in_media_mode():
    query = compose_query("site:linkedin.com/in", mode="media", domain="example.com", keyword="")
    assert query == "site:linkedin.com/in"


def test_build_google_url_encodes_query():
    url = build_google_url("site:example.com \"quarterly report\" filetype:pdf")
    assert url.startswith("https://www.google.com/search?q=")
    assert "quarterly+report" in url
