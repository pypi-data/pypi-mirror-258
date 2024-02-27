"""
Module supporting 'qbraid jobs enable/disable braket' and commands.

"""

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple

import typer

from qbraid_cli.exceptions import QbraidException
from qbraid_cli.handlers import handle_error, handle_filesystem_operation, run_progress_task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_package_data(package: str) -> Tuple[str, str, str]:
    """Retrieve package version and location data.

    Args:
        package (str): The name of the package to retrieve data for.

    Returns:
        Tuple[str, str, str]: The installed and latest versions of the package, and the
                              local site-packages path where it is / would be installed.

    Raises:
        QbraidException: If package version or location data cannot be retrieved.

    """
    from qbraid.api.system import (
        get_active_site_packages_path,
        get_latest_package_version,
        get_local_package_version,
    )
    from qbraid.exceptions import QbraidError

    try:
        installed_version = get_local_package_version(package)
        latest_version = get_latest_package_version(package)
    except QbraidError as err:
        raise QbraidException("Failed to retrieve package version information") from err

    try:
        site_packages_path = get_active_site_packages_path()
    except QbraidError as err:
        raise QbraidException("Failed to retrieve site-package location") from err

    return installed_version, latest_version, site_packages_path


def confirm_updates(
    mode: str,
    site_packages_path: str,
    installed_version: Optional[str] = None,
    latest_version: Optional[str] = None,
) -> None:
    """
    Prompts the user to proceed with enabling or disabling qBraid Quantum Jobs.

    Args:
        mode (str): The mode of operation, either "enable" or "disable".
        site_packages_path (str): The location of the site-packages directory where
                                  target package(s) will be updated.
        installed_version (optional, str): The installed version of the target package.
        latest_version (optional, str): The latest version of the target package available on PyPI.

    Returns:
        None

    Raises:
        ValueError: If an invalid mode is provided.
        typer.Exit: If the user declines to proceed with enabling or disabling qBraid Quantum Jobs.

    """
    core_package = "botocore"
    versioned_package = "boto3"
    if mode == "enable":
        provider = "qBraid"
        update_msg = f"update {versioned_package} and install"
    elif mode == "disable":
        provider = "boto"
        update_msg = "re-install"
    else:
        raise ValueError(f"Invalid mode: {mode}. Expected 'enable' or 'disable'.")

    typer.echo(f"\n==> WARNING: {provider}/{core_package} package required <==")
    if (
        installed_version is not None
        and latest_version is not None
        and installed_version != latest_version
    ):
        typer.echo(f"==> WARNING: A newer version of {versioned_package} exists. <==")
        typer.echo(f"  current version: {installed_version}")
        typer.echo(f"  latest version: {latest_version}")

    gerund = mode[:-2].capitalize() + "ing"

    typer.echo(
        f"\n{gerund} quantum jobs will automatically {update_msg} {provider}/{core_package}, "
        "which may cause incompatibilities with the amazon-braket-sdk and/or awscli.\n"
    )
    typer.echo("## Package Plan ##")
    if mode == "enable":
        typer.echo(
            f"  {versioned_package} location: {os.path.join(site_packages_path, versioned_package)}"
        )
    typer.echo(f"  {core_package} location: {os.path.join(site_packages_path, core_package)}\n")

    user_confirmation = typer.confirm("Proceed", default=True)
    if not user_confirmation:
        typer.echo("\nqBraidSystemExit: Exiting.")
        raise typer.Exit()

    typer.echo("")


def aws_configure_dummy() -> None:
    """
    Initializes AWS configuration and credentials files with placeholder values.

    This function ensures the existence of AWS config and credentials files in the user's home
    directory. If these files do not already exist, it creates them and populates them with
    placeholder values for the AWS access key and secret access key. While AWS credentials are not
    required when submitting quantum tasks through qBraid, Amazon Braket requires these files to be
    present to prevent configuration errors.
    """
    aws_dir = Path.home() / ".aws"
    config_path = aws_dir / "config"
    credentials_path = aws_dir / "credentials"

    def configure_aws():
        aws_dir.mkdir(exist_ok=True)
        if not config_path.exists():
            config_content = "[default]\nregion = us-east-1\noutput = json\n"
            config_path.write_text(config_content)
        if not credentials_path.exists():
            access_key, secret_key = "MYACCESSKEY", "MYSECRETKEY"
            credentials_content = (
                f"[default]\n"
                f"aws_access_key_id = {access_key}\n"
                f"aws_secret_access_key = {secret_key}\n"
            )
            credentials_path.write_text(credentials_content)

    try:
        handle_filesystem_operation(configure_aws, aws_dir)
    except QbraidException:
        handle_error(message="Failed to configure qBraid quantum jobs.")


def enable_braket():
    """Enable qBraid quantum jobs for Amazon Braket."""
    installed_version, latest_version, site_packages_path = run_progress_task(
        get_package_data, "boto3", description="Solving environment..."
    )
    confirm_updates("enable", site_packages_path, installed_version, latest_version)
    aws_configure_dummy()  # TODO: possibly add another confirmation for writing aws config files

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "boto3"])
        subprocess.check_call(
            [sys.executable, "-m", "pip", "uninstall", "botocore", "-y", "--quiet"]
        )
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "git+https://github.com/qBraid/botocore.git"]
        )
    except subprocess.CalledProcessError:
        handle_error(message="Failed to enable qBraid quantum jobs.")

    typer.secho("\nSuccessfully enabled qBraid quantum jobs.", fg=typer.colors.GREEN, bold=True)
    typer.secho(
        "\nTo disable, run: `qbraid jobs disable braket`\n", fg=typer.colors.GREEN, bold=True
    )


def disable_braket():
    """Disable qBraid quantum jobs for Amazon Braket."""
    package = "botocore"
    installed_version, latest_version, site_packages_path = run_progress_task(
        get_package_data, package, description="Solving environment..."
    )
    package = f"{package}~={installed_version}" if installed_version < latest_version else package
    confirm_updates("disable", site_packages_path)

    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                package,
                "--force-reinstall",
            ],
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        handle_error(message="Failed to disable qBraid quantum jobs.")

    typer.secho("\nSuccessfully disabled qBraid quantum jobs.", fg=typer.colors.GREEN, bold=True)
    typer.secho("\nTo enable, run: `qbraid jobs enable braket`\n", fg=typer.colors.GREEN, bold=True)
