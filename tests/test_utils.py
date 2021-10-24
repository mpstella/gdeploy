from gdeploy.helpers.utils import (
    dict_to_sorted_list,
    list_to_dict,
    merge_collections,
    collection_items,
)


def test_dict_to_sorted_list():
    d = {"a": "1", "c": "2", "z": 3, "b": 4}
    actual = dict_to_sorted_list(d)
    expected = [("a", "1"), ("b", 4), ("c", "2"), ("z", 3)]
    assert expected == actual


def test_list_to_dict():
    l = ["a", "b", "c"]
    actual = list_to_dict(l)
    expected = {"a": "a", "b": "b", "c": "c"}
    assert expected == actual


def test_merge_collections():
    # depending on the order one will be replaced
    c1 = ["a", "b", "c"]
    c2 = {"d": 1, "e": 2, "c": 3}

    # c2.c will overwrite c1.c
    actual = merge_collections(c1, c2)
    expected = {"a": "a", "b": "b", "c": 3, "d": 1, "e": 2}
    assert expected == actual

    # c1.c will overwrite c2.c
    actual = merge_collections(c2, c1)
    expected = {"a": "a", "b": "b", "c": "c", "d": 1, "e": 2}
    assert expected == actual


def test_collection_items():
    c1 = ["a", "b", "c"]
    c2 = {"d": 1, "e": 2, "f": 3}
    expected = [("a", "a"), ("b", "b"), ("c", "c"), ("d", 1), ("e", 2), ("f", 3)]
    actual = list(collection_items(c1, c2))
    assert expected == actual
