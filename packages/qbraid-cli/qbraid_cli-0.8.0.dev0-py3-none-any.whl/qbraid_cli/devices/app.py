"""
Module defining commands in the 'qbraid devices' namespace.

"""

from typing import Callable, Optional, Tuple, Union

import typer

from qbraid_cli.handlers import handle_error, run_progress_task, validate_item

app = typer.Typer(help="Manage qBraid quantum devices.")


def validate_status(value: Optional[str]) -> Union[str, None]:
    """Validate device status query parameter."""
    return validate_item(value, ["ONLINE", "OFFLINE", "RETIRED"], "Status")


def validate_type(value: Optional[str]) -> Union[str, None]:
    """Validate device type query parameter."""
    return validate_item(value, ["QPU", "SIMULATOR"], "Type")


def validate_provider(value: Optional[str]) -> Union[str, None]:
    """Validate device provider query parameter."""
    return validate_item(value, ["AWS", "IBM", "IonQ", "Rigetti", "OQC", "QuEra"], "Provider")


@app.command(name="list")
def devices_list(
    status: Optional[str] = typer.Option(
        None, "--status", "-s", help="'ONLINE'|'OFFLINE'|'RETIRED'", callback=validate_status
    ),
    device_type: Optional[str] = typer.Option(
        None, "--type", "-t", help="'QPU'|'SIMULATOR'", callback=validate_type
    ),
    provider: Optional[str] = typer.Option(
        None,
        "--provider",
        "-p",
        help="'AWS'|'IBM'|'IonQ'|'Rigetti'|'OQC'|'QuEra'",
        callback=validate_provider,
    ),
) -> None:
    """List qBraid quantum devices."""

    def import_devices() -> Tuple[Callable, Exception]:
        from qbraid import get_devices
        from qbraid.exceptions import QbraidError

        return get_devices, QbraidError

    result: Tuple[Callable, Exception] = run_progress_task(import_devices)
    get_devices, QbraidError = result

    filters = {}
    if status:
        filters["status"] = status
    if device_type:
        filters["type"] = "Simulator" if device_type == "SIMULATOR" else device_type
    if provider:
        filters["provider"] = provider

    try:
        get_devices(filters=filters)
    except QbraidError:
        handle_error(message="Failed to fetch quantum devices.")


if __name__ == "__main__":
    app()
