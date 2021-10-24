import subprocess
from os import makedirs
from pathlib import Path
import platform

from typing import List, Dict, Union


class TerminalException(Exception):
    def __init__(self, command: str, message: str, rc: int) -> None:

        self.command = command
        self.message = (
            message.strip() if isinstance(message, str) else (" ".join(message)).strip()
        )
        self.rc = rc
        super().__init__(message)

    def __str__(self) -> str:
        return f"Command '{self.command}' failed with rc=({self.rc}) and message: {self.message}"


class DirectoryOrFileNotFoundException(Exception):
    def __init__(self, path: str) -> None:
        super().__init__(
            f"The following directory or file could not be found: '{path}'"
        )


def operating_system() -> str:
    """Retrieve the current Operating System

    Returns:
        str: the operating system (Darwin, Windows or Linux)
    """
    return platform.system()


def is_darwin() -> bool:
    """Determine if running on Darwin (OSX)

    Returns:
        bool: True if Darwin, otherwise False
    """
    return operating_system() == "Darwin"


def is_windows() -> bool:
    """Determine if running on Windows

    Returns:
        bool: True if Windows, otherwise False
    """
    return operating_system() == "Windows"


def is_linux() -> bool:
    """Determine if running on Linux

    Returns:
        bool: True if Linux, otherwise False
    """
    return operating_system() == "Linux"


def check_path(path: Union[Path, str], create=False) -> Path:
    """Determines whether a path exists, optionally create it if specified

    Args:
        path (Union[Path, str]): the path
        create (bool): If set to True, create the path if it does not exist

    Returns:
        Path: Path object

    Raises:
        DirectoryOrFileNotFoundException: If path does not exist and should not be created
    """
    _path = path if isinstance(path, Path) else Path(path)

    if _path.exists():
        return _path

    if create:
        makedirs(_path)
        return check_path(_path, create=False)

    raise DirectoryOrFileNotFoundException(_path)


def run_cmd(
    cmd: Union[List[str], str],
    env: Dict[str, str] = None,
    working_dir: Union[Path, str] = None,
) -> List[str]:
    """Run a shell command

    Args:
        cmd (Union[List[str], str]): The actual command to execute
        env (Dict[str, str]): Optional dictionary to add to running Environment (variables)
        working_dir: (Union[Path, str]): Optional directory to switch to prior to executing cmd

    Returns:
        List[str]: The command output

    Raises:
        TerminalException: If any exception occurs or non zero RC
    """

    def ensure_array(v):
        return v.split(" ") if isinstance(v, str) else v

    _cmd = [str(c) for c in ensure_array(cmd)]

    try:

        if working_dir is not None:
            check_path(working_dir)

        return (
            subprocess.check_output(
                _cmd,
                stderr=subprocess.STDOUT,
                env=env,
                cwd=working_dir,
                shell=is_windows(),
            )
            .decode("utf-8")
            .splitlines()
        )

    except subprocess.CalledProcessError as e:
        raise TerminalException(
            command=cmd, message=e.output.decode("utf-8"), rc=e.returncode
        )
