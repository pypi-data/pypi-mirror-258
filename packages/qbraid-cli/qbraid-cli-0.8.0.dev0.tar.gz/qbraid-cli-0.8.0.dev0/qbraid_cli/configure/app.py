"""
Module defining commands in the 'qbraid configure' namespace.

"""

import configparser
import re
from copy import deepcopy
from pathlib import Path
from typing import Dict, Optional

import typer

from qbraid_cli.exceptions import QbraidException
from qbraid_cli.handlers import handle_filesystem_operation

# disable pretty_exceptions_show_locals to avoid printing sensative information in the traceback
app = typer.Typer(help="Configure qBraid CLI options.", pretty_exceptions_show_locals=False)


def load_config() -> configparser.ConfigParser:
    """Load the configuration from the file."""
    config_path = Path.home() / ".qbraid" / "qbraidrc"
    config = configparser.ConfigParser()
    try:
        config.read(config_path)
        if not config.sections():
            raise QbraidException(f"No sections found in configuration file {config_path}")
        return config
    except (FileNotFoundError, PermissionError, configparser.Error) as err:
        raise QbraidException(f"Failed to load configuration from {config_path}.") from err


def save_config(config: configparser.ConfigParser) -> None:
    """Save configuration to qbraidrc file."""
    config_path = Path.home() / ".qbraid"

    def save_operation():
        config_path.mkdir(parents=True, exist_ok=True)
        with (config_path / "qbraidrc").open("w") as configfile:
            config.write(configfile)

    handle_filesystem_operation(save_operation, config_path)


def validate_input(key: str, value: str) -> str:
    """Validate the user input based on the key.

    Args:
        key (str): The configuration key
        value (str): The user input value

    Returns:
        str: The validated value

    Raises:
        typer.BadParameter: If the value is invalid
    """
    if key == "url":
        if not re.match(r"^https?://\S+$", value):
            raise typer.BadParameter("Invalid URL format.")
    elif key == "email":
        if not re.match(r"^\S+@\S+\.\S+$", value):
            raise typer.BadParameter("Invalid email format.")
    elif key == "api-key":
        if not re.match(r"^[a-zA-Z0-9]{11}$", value):
            raise typer.BadParameter("Invalid API key format.")
    return value


def prompt_for_config(
    config: configparser.ConfigParser,
    section: str,
    key: str,
    default_values: Optional[Dict[str, str]] = None,
) -> str:
    """Prompt the user for a configuration setting, showing the current value as default."""
    default_values = default_values or {}
    current_value = config.get(section, key, fallback=default_values.get(key, ""))
    display_value = "None" if not current_value else current_value

    if key == "api-key" and current_value:
        display_value = "*" * len(current_value[:-4]) + current_value[-4:]

    new_value = typer.prompt(f"Enter {key}", default=display_value, show_default=True).strip()

    if new_value == display_value:
        return current_value

    return validate_input(key, new_value)


def default_action(section: str = "default"):
    """Configure qBraid CLI options."""
    config = load_config()
    original_config = deepcopy(config)

    if section not in config:
        config[section] = {}

    default_values = {"url": "https://api.qbraid.com/api"}

    config[section]["url"] = prompt_for_config(config, section, "url", default_values)
    config[section]["email"] = prompt_for_config(config, section, "email", default_values)
    config[section]["api-key"] = prompt_for_config(config, section, "api-key", default_values)

    for key in list(config[section]):
        if not config[section][key]:
            del config[section][key]

    if config == original_config:
        typer.echo("\nConfiguration saved, unchanged.")
    else:
        save_config(config)
        typer.echo("\nConfiguration updated successfully.")


@app.callback(invoke_without_command=True)
def configure(ctx: typer.Context):
    """
    Prompts user for configuration values such as your qBraid API Key.
    If your config file does not exist (the default location is ~/.qbraid/qbraidrc),
    the qBraid CLI will create it for you. To keep an existing value, hit enter
    when prompted for the value. When you are prompted for information, the current
    value will be displayed in [brackets]. If the config item has no value, it be
    displayed as [None].

    """
    if ctx.invoked_subcommand is None:
        default_action()


@app.command(name="set")
def configure_set(
    name: str = typer.Argument(..., help="Config name"),
    value: str = typer.Argument(..., help="Config value"),
    profile: str = typer.Option("default", help="Profile name"),
):
    """Set configuration value in qbraidrc file."""
    config = load_config()

    if profile not in config:
        config[profile] = {}

    config[profile][name] = value

    save_config(config)
    typer.echo("Configuration updated successfully.")


if __name__ == "__main__":
    app()
