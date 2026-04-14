from dorkgen import DorkRequest, __version__, build_dorks


def test_package_exports_expected_api():
    req = DorkRequest(objective_key="public-documents")
    results = build_dorks(req)

    assert isinstance(results, list)
    assert results
    assert isinstance(__version__, str)
