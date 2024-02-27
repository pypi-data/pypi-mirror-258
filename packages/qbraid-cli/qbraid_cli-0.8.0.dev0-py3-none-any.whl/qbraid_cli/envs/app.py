"""
Module defining commands in the 'qbraid envs' namespace.

"""

import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import typer
from rich.console import Console

from qbraid_cli.handlers import QbraidException, run_progress_task

app = typer.Typer(help="Manage qBraid environments.")


def installed_envs_data() -> Tuple[Dict[str, Path], Dict[str, str]]:
    """Gather paths and aliases for all installed qBraid environments."""
    from qbraid.api.system import get_qbraid_envs_paths, is_valid_slug

    installed = {}
    aliases = {}

    qbraid_env_paths: List[Path] = get_qbraid_envs_paths()

    for env_path in qbraid_env_paths:
        for entry in env_path.iterdir():
            if entry.is_dir() and is_valid_slug(entry.name):
                installed[entry.name] = entry

                if entry.name == "qbraid_000000":
                    aliases["default"] = entry.name
                    continue

                state_json_path = entry / "state.json"
                if state_json_path.exists():
                    try:
                        with open(state_json_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        aliases[data.get("name", entry.name[:-7])] = entry.name
                    # pylint: disable-next=broad-exception-caught
                    except (json.JSONDecodeError, Exception):
                        aliases[entry.name[:-7]] = entry.name
                else:
                    aliases[entry.name[:-7]] = entry.name

    return installed, aliases


@app.command(name="create")
def envs_create(
    name: str = typer.Option(..., "--name", "-n", help="Name of the environment to create"),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Short description of the environment"
    ),
) -> None:
    """Create a new qBraid environment.

    NOTE: Requires updated API route from https://github.com/qBraid/api/pull/482,
    This command will not work until that PR is merged, and the updates are deployed.
    """
    from .create import create_qbraid_env

    def request_new_env(req_body: Dict[str, str]) -> str:
        """Send request to create new environment and return the slug."""
        from qbraid.api import QbraidSession, RequestsApiError

        session = QbraidSession()

        try:
            resp = session.post("/environments/create", json=req_body).json()
        except RequestsApiError as err:
            raise QbraidException("Create environment request failed") from err

        slug = resp.get("slug")
        if slug is None:
            raise QbraidException(f"Create environment request returned invalid slug, {slug}")

        return slug

    req_body = {
        "name": name,
        "description": description or "",
        "tags": "",  # comma separated list of tags
        "code": "",  # newline separated list of packages
        "visibility": "private",
        "kernelName": "",
        "prompt": "",
    }
    slug = run_progress_task(
        request_new_env,
        req_body,
        description="Validating...",
        error_message="Failed to create qBraid environment",
    )

    run_progress_task(
        create_qbraid_env,
        slug,
        name,
        description="Creating qBraid environment...",
        error_message="Failed to create qBraid environment",
    )

    # TODO: Add the command they can use to activate the environment to end of success message
    console = Console()
    console.print(
        f"\n[bold green]Successfully created qBraid environment: "
        f"[/bold green][bold magenta]{name}[/bold magenta]\n"
    )


@app.command(name="delete")
def envs_delete(name: str = typer.Argument(..., help="Name of the environment to delete")) -> None:
    """Delete a qBraid environment.

    NOTE: Requires updated API route from https://github.com/qBraid/api/pull/482,
    This command will not work until that PR is merged, and the updates are deployed.
    """

    def request_delete_env(name: str) -> str:
        """Send request to create new environment and return the slug."""
        from qbraid.api import QbraidSession, RequestsApiError

        session = QbraidSession()

        installed, aliases = installed_envs_data()
        for alias, slug_name in aliases.items():
            if alias == name:
                slug = slug_name
                path = installed[slug_name]

                try:
                    session.delete(f"/environments/{slug}")
                except RequestsApiError as err:
                    raise QbraidException("Create environment request failed") from err

                return path

        raise QbraidException(f"Environment '{name}' not found.")

    path = run_progress_task(
        request_delete_env,
        name,
        description="Deleting remote environment data...",
        error_message="Failed to delete qBraid environment",
    )

    run_progress_task(
        shutil.rmtree,
        path,
        description="Deleting local environment...",
        error_message="Failed to delete qBraid environment",
    )

    console = Console()
    console.print(
        f"\n[bold green]Successfully delete qBraid environment: "
        f"[/bold green][bold magenta]{name}[/bold magenta]\n"
    )


@app.command(name="list")
def envs_list():
    """List installed qBraid environments."""
    installed, aliases = installed_envs_data()

    if len(installed) == 0:
        print("No qBraid environments installed.")
        print("\nUse 'qbraid envs create' to create a new environment.")
        return

    alias_path_pairs = [(alias, installed[slug_name]) for alias, slug_name in aliases.items()]

    sorted_alias_path_pairs = sorted(
        alias_path_pairs,
        key=lambda x: (x[0] != "default", str(x[1]).startswith(str(Path.home())), x[0]),
    )

    current_env_path = Path(sys.executable).parent.parent.parent

    max_alias_length = (
        max(len(alias) for alias, _ in sorted_alias_path_pairs) if sorted_alias_path_pairs else 0
    )
    max_path_length = (
        max(len(str(path)) for _, path in sorted_alias_path_pairs) if sorted_alias_path_pairs else 0
    )

    print("# installed environments:")
    print("#")
    print("")
    for alias, path in sorted_alias_path_pairs:
        mark = "*  " if path == current_env_path else "   "
        print(f"{alias.ljust(max_alias_length + 11)}{mark}{str(path).ljust(max_path_length)}")


@app.command(name="activate")
def envs_activate(
    name: str = typer.Argument(..., help="Name of the environment. Values from 'qbraid envs list'.")
):
    """Activate qBraid environment.

    NOTE: Currently only works on qBraid Lab platform, and select few other OS types.
    """
    installed, aliases = installed_envs_data()
    if name in aliases:
        venv_path: Path = installed[aliases[name]] / "pyenv"
    elif name in installed:
        venv_path: Path = installed[name] / "pyenv"
    else:
        raise typer.BadParameter(f"Environment '{name}' not found.")

    from .activate import activate_pyvenv

    activate_pyvenv(venv_path)


if __name__ == "__main__":
    app()
