from pathlib import Path

import pytest

from gdeploy.helpers.config_reader import (
    read_jsonnet,
    read_json,
    read_config,
    UnsupportedConfiguration,
)


@pytest.fixture()
def data_dir():
    d = Path(__file__).parents[0]
    return d / "data"


def test_jsonnet_to_json_simple(data_dir: Path) -> None:

    conf = data_dir / "simple.jsonnet"
    actual = read_jsonnet(conf)
    expected = {"Hello": "World"}

    assert expected == actual


def test_json(data_dir) -> None:
    conf = data_dir / "simple.json"
    actual = read_json(conf)
    expected = {"Hello": "World"}

    assert expected == actual


def test_read_config(data_dir) -> None:
    expected = {"Hello": "World"}

    simple_jsonnet_conf = data_dir / "simple.jsonnet"

    actual = read_config(simple_jsonnet_conf)
    assert expected == actual

    simple_json_conf = data_dir / "simple.json"
    actual = read_config(simple_json_conf)
    assert expected == actual

    unsupported_conf = data_dir / "unsupported.file"

    with pytest.raises(UnsupportedConfiguration):
        read_config(unsupported_conf)
