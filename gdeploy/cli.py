import typer

from gdeploy import VERSION
from gdeploy.functions import commands
from gdeploy.gcloud.cmd import Cmd

app = typer.Typer(add_completion=False)
app.add_typer(
    commands.app, name="functions", short_help="Wrapper for `gcloud functions`"
)


@app.command()
def auth():
    """This is an example that does a `gcloud auth list`"""
    typer.Exit(Cmd("auth", "list").run())


@app.command()
def version():
    """Print the current version"""
    typer.secho(
        f"{str(__name__).split('.')[0]} {VERSION}", fg=typer.colors.GREEN, bold=True
    )
    typer.echo("\n".join(Cmd.version()))


if __name__ == "__main__":
    app()
