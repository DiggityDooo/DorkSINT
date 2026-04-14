from dorkgen.builder import DorkRequest, build_dorks


def test_build_dorks_returns_multiple_variants():
    req = DorkRequest(
        objective_key="public-documents",
        domain="example.com",
        keyword="payroll",
        filetypes=["pdf", "docx"],
        exclude_terms=["sample"],
    )
    results = build_dorks(req)

    assert len(results) >= 3
    assert results[0].startswith("site:example.com")
    assert any("intitle:" in query for query in results)
    assert all("-sample" in query for query in results)


def test_open_directory_variant_included_for_backups():
    req = DorkRequest(objective_key="public-backups", domain="example.com")
    results = build_dorks(req)

    assert any("\"parent directory\"" in query for query in results)

