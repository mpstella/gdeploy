from typing import List, Callable, Dict, Any, Optional, Tuple

import typer

from gdeploy import EXIT_SUCCESS, EXIT_FAILURE
from gdeploy.helpers.utils import dict_to_sorted_list, collection_items
from gdeploy import term


def string_arg(name: str) -> Callable[[str], List[str]]:
    def get(value: str) -> List[str]:
        return [f"--{name}={value}"]

    return get


def map_arg(name: str) -> Callable[[Dict[str, str]], List[str]]:
    def get(value: Dict[str, str] = None) -> List[str]:
        d = [f"{k}={v}" for k, v in dict_to_sorted_list(value)]
        return [f"--{name}", ",".join(d)]

    return get


def listmap_arg(name: str) -> Callable[[List[str]], List[str]]:
    def get(value: List[str] = None) -> List[str]:
        return [f"--{name}=[{','.join(value)}]"]

    return get


def flag_arg(name: str) -> Callable[[], List[str]]:
    def get(_=None) -> List[str]:
        return [f"--{name}"]

    return get


class Cmd:
    GCLOUD_CMD = "gcloud"

    def __init__(self, *args) -> None:
        self.__runtime_args = args

    @staticmethod
    def version() -> List[str]:
        return term.run_cmd([Cmd.GCLOUD_CMD, "version"])

    def __build(self, args: Dict[str, str], flags: List[str]) -> List[str]:

        mapping = self.__map_args(args, flags)

        _c = [self.GCLOUD_CMD, *self.__runtime_args]
        _a = []

        for k, v in collection_items(args, flags):
            _a += mapping[k](v)

        _c += list(map("".join, _a))

        return _c

    @staticmethod
    def __map_args(
        args: Dict[str, Any], flags: List[str]
    ) -> Dict[str, Callable[[Optional[Any]], List[str]]]:

        mapping = {}

        def add_mapping(name: str, func: Callable[[Optional[Any]], List[str]]) -> None:
            mapping[name] = func

        for k, v in args.items():
            if isinstance(v, dict):
                add_mapping(k, map_arg(k))
            elif isinstance(v, list):
                add_mapping(k, listmap_arg(k))
            else:
                add_mapping(k, string_arg(k))

        for f in flags:
            add_mapping(f, flag_arg(f))

        return mapping

    def run(self, args: Dict[str, Any] = None, flags: List[str] = None) -> int:
        try:

            _out = term.run_cmd(self.__build(args or {}, flags or []))
            typer.echo("\n".join(_out))
            return EXIT_SUCCESS
        except term.TerminalException as e:
            typer.secho(
                "An error has occurred", fg=typer.colors.RED, bold=True, err=True
            )
            typer.echo(str(e), err=True)
            return EXIT_FAILURE
