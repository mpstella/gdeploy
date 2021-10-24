from pathlib import Path

import typer

from gdeploy.gcloud.cmd import Cmd
from gdeploy.helpers.config_reader import (
    read_config,
    UnsupportedConfiguration,
    InvalidConfigurationException,
    MissingJsonnetExec,
)

app = typer.Typer()


@app.command(name="deploy")
def deploy_function(
    config: Path = typer.Option(
        ...,
        exists=True,
        resolve_path=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        envvar="CONFIG_PATH",
        help="Path to Jsonnet/JSON configuration file",
    ),
    source: Path = typer.Option(
        "src",
        exists=True,
        resolve_path=True,
        readable=True,
        file_okay=False,
        dir_okay=True,
        envvar="SOURCE_PATH",
        help="Path to the function source code",
    ),
) -> None:
    """
    Wrapper around `gcloud functions deploy`
    """
    typer.echo(f"gcloud functions deploy config='{config}' source='{source}' ...")

    try:

        _config = read_config(config)

        name = _config["name"]  # mandatory
        args = _config["args"]  # args is required, even if empty
        flags = _config.get("flags", [])  # not required
        opts = _config.get("opts", [])  # not required

        # add source to args for gcloud
        args["source"] = source

        raise typer.Exit(Cmd(*opts, "functions", "deploy", name).run(args, flags))

    except KeyError as e:
        typer.secho(
            f"Missing configuration item {e}", err=True, fg=typer.colors.RED, bold=True
        )
        raise typer.Abort()
    except MissingJsonnetExec as e:
        typer.secho(str(e), err=True, fg=typer.colors.RED, bold=True)
        raise typer.Abort()
    except (UnsupportedConfiguration, InvalidConfigurationException) as e:
        typer.secho(
            "A Configuration Error has occurred",
            err=True,
            fg=typer.colors.RED,
            bold=True,
        )
        typer.echo(str(e), err=True)
        raise typer.Abort()


@app.command(name="list")
def list_functions() -> None:
    """A wrapper for `gcloud functions list`"""
    raise typer.Exit(Cmd("functions", "list").run())
