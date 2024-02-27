"""
Module defining commands in the 'qbraid credits' namespace.

"""

import typer

from qbraid_cli.handlers import run_progress_task

app = typer.Typer(help="Manage qBraid credits.")


@app.command(name="value")
def credits_value():
    """Get number of qBraid credits remaining."""

    def get_credits() -> int:
        from qbraid.api import QbraidSession

        session = QbraidSession()
        res = session.get("/billing/credits/get-user-credits").json()
        return res["qbraidCredits"]

    qbraid_credits: int = run_progress_task(get_credits)
    credits_text = typer.style(str(qbraid_credits), fg=typer.colors.GREEN, bold=True)
    typer.secho(f"\nqBraid credits: {credits_text}")


if __name__ == "__main__":
    app()
