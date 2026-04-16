from dorkgen.catalog import get_by_id, list_categories, load_catalog


def test_load_catalog_defaults_to_security_mode_only():
    items = load_catalog(include_file_hunter=False)
    assert items
    assert all(item.mode == "sec" for item in items)


def test_load_catalog_includes_media_when_enabled():
    items = load_catalog(include_file_hunter=True)
    assert any(item.mode == "media" for item in items)
    assert any(item.mode == "sec" for item in items)


def test_catalog_ids_are_unique():
    items = load_catalog(include_file_hunter=True)
    ids = [item.id for item in items]
    assert len(ids) == len(set(ids))


def test_get_by_id_finds_expected_item():
    items = load_catalog(include_file_hunter=False)
    item = get_by_id(items, "sec.attack-surface-mapping.exposed-login-endpoints")
    assert item is not None
    assert item.category == "Attack Surface Mapping"


def test_list_categories_keeps_order():
    items = load_catalog(include_file_hunter=False)
    categories = list_categories(items, mode="sec")
    assert categories[0] == "Attack Surface Mapping"
