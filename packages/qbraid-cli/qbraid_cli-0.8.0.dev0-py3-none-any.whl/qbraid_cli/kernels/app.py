"""
Module defining commands in the 'qbraid jobs' namespace.

"""

import subprocess

import typer

from qbraid_cli.handlers import handle_error

app = typer.Typer(help="Manage qBraid kernels.")


@app.command(name="list")
def kernels_list():
    """List all available kernels."""
    try:
        result = subprocess.run(
            ["jupyter", "kernelspec", "list"], capture_output=True, text=True, check=True
        )

        print(result.stdout)
    except subprocess.CalledProcessError:
        handle_error("Failed to list kernels.")


if __name__ == "__main__":
    app()
