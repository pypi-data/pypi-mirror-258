"""
Entrypoint for the qBraid CLI.

"""

import typer

from .configure import app as configure_app
from .credits import app as credits_app
from .devices import app as devices_app
from .envs import app as envs_app
from .jobs import app as jobs_app
from .kernels import app as kernels_app

app = typer.Typer()
app.add_typer(configure_app, name="configure")
app.add_typer(envs_app, name="envs")
app.add_typer(jobs_app, name="jobs")
app.add_typer(devices_app, name="devices")
app.add_typer(kernels_app, name="kernels")
app.add_typer(credits_app, name="credits")


def version_callback(value: bool):
    """Show the version and exit."""
    if value:
        from ._version import __version__

        typer.echo(f"qbraid-cli/{__version__}")
        raise typer.Exit()


def show_banner():
    """Show the qBraid CLI banner."""
    typer.secho("----------------------------------", fg=typer.colors.BRIGHT_BLACK)
    typer.secho("  * ", fg=typer.colors.BRIGHT_BLACK, nl=False)
    typer.secho("Welcome to the qBraid CLI!", fg=typer.colors.MAGENTA, nl=False)
    typer.secho(" * ", fg=typer.colors.BRIGHT_BLACK)
    typer.secho("----------------------------------", fg=typer.colors.BRIGHT_BLACK)
    typer.echo("")
    typer.echo("        ____            _     _  ")
    typer.echo("   __ _| __ ) _ __ __ _(_) __| | ")
    typer.echo(r"  / _` |  _ \| '__/ _` | |/ _` | ")
    typer.echo(" | (_| | |_) | | | (_| | | (_| | ")
    typer.echo(r"  \__,_|____/|_|  \__,_|_|\__,_| ")
    typer.echo("     |_|                         ")
    typer.echo("")
    typer.echo("")
    typer.echo("- Use 'qbraid --help' to see available commands.")
    typer.echo("")
    typer.echo("- Use 'qbraid --version' to see the current version.")
    typer.echo("")
    typer.echo("Reference Docs: https://docs.qbraid.com/projects/cli/en/latest/cli/qbraid.html")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
):
    """The qBraid CLI."""
    if ctx.invoked_subcommand is None and not version:
        show_banner()


if __name__ == "__main__":
    app()
