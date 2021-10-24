import json
import os
from pathlib import Path
from typing import Dict, Any
from gdeploy import term


class UnsupportedConfiguration(Exception):
    def __init__(self, path: Path) -> None:
        super().__init__(
            f"The following configuration extension is not support: '{path.suffix}'"
        )


class InvalidConfigurationException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class MissingJsonnetExec(Exception):
    def __init__(self) -> None:
        super().__init__("Jsonnet executable not found")


def invalid_config(path: Path) -> None:
    raise UnsupportedConfiguration(path)


def read_config(path: Path) -> Dict[str, Any]:
    """A helper function to read configuration files

    Note: If using Jsonnet and ExtVar this *does* not support it

    Args:
        path (Path): The path to the config file

    Returns:
        Dict[str, Any]: The final evaluated Json (python Dictionary)
    """
    reader = CONFIG_MAPPING.get(path.suffix.lower(), invalid_config)

    try:
        return reader(path)
    except RuntimeError as e:
        raise InvalidConfigurationException(str(e))


def __check_jsonnet() -> None:
    try:
        term.run_cmd(["jsonnet", "-v"])
    except FileNotFoundError:
        raise MissingJsonnetExec()


def read_jsonnet(path: Path) -> Dict[str, Any]:
    """Reads a Jsonnet file and returns a Python dictionary

    * Note, this assumes jsonnet is installed on your machine and accessible via PATH

    Args:
        path (Path): The path to the Jsonnet file

    Returns:
        Dict[str, Any]: The final evaluated Json (python Dictionary)
    """

    __check_jsonnet()

    import datetime

    ts = str(datetime.datetime.now().timestamp()).replace(".", "_")
    json_file = path.parents[0] / f"{ts}_{path.stem}.json"

    try:

        cmd = ["jsonnet", str(path), "-o", json_file]
        term.run_cmd(cmd)
        return read_json(json_file)

    finally:
        if json_file.exists():
            os.remove(json_file)


def read_json(path: Path) -> Dict[str, Any]:
    """Reads a JSON file and returns a Python dictionary

    Args:
        path (Path): The path to the json file

    Returns:
        Dict[str, Any]: The final evaluated Json (python Dictionary)
    """
    with open(path) as f:
        return json.load(f)


CONFIG_MAPPING = {".json": read_json, ".jsonnet": read_jsonnet}
