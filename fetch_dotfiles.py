import argparse
import json
from pathlib import Path
from typing import Optional

SELF_PATH = Path(__file__).parents[0]
CONFIG_REPO = SELF_PATH / "config_repo"
CONFIG_PATH = CONFIG_REPO / "dotfiles.json"

ROOT_JSON = "dotfiles"


class Deployment:
    deployment_name: str
    deployment_path: Path
    storage_path: Optional[Path]
    valid: bool = False


def __post_init__(self):
    if not self.deployment_path.exists():
        print(f"[!] Config for {self.name}@{self.deployment_path.as_posix()} "
              f"does not exist. Skipping processing for {self.name}")

    elif self.storage_path is not None:
        if not self.storage_path.exists():
            print(f"[!] Storage path specified for "
                  f"{self.name}@{self.storage_path.as_posix()} does not exist."
                  f" Skipping processing for {self.name}")


def main():
    args = _get_args()
    config_file = _get_config()

    _parse_config_file(config_file)


def _parse_config_file(config_file: dict) -> None:
    """
    Iterate over the config dictionary and attempt to convert each deployment
    unit to a Deployment object.
    :param config_file: Dictionary containing the deployment units
    :return: None
    :rtype: None
    """
    if not config_file.get(ROOT_JSON):
        exit("[!] INVALID JSON FORMAT: dotfiles.json missing root key "
             f"\"{ROOT_JSON}\" located at {CONFIG_PATH.as_posix()}")

    # Iterate over all the deployment units
    for deployment, d_units in config_file[ROOT_JSON].items():
        # Each deployment unit MUST have their own repo path
        deployment_path = _set_config_repo(deployment)

        # Iterate over each deployment unit for the unit and varify that
        # the paths exist before creating a deployment object
        for dotfile in d_units:
            for unit, paths in dotfile.items():
                _set_unit_repo(deployment_path, unit)


def _set_unit_repo(deployment_path: Path, unit: str) -> None:
    """
    Create the path to the deployment unit using the deployment path.

    :Example:
    If Tmux is a Deployment named tmux, the tmux repo will be created as
    tmux_repo.

    Tmux in most cases just has a single file, the tmux.conf. If the
    Deployment Unit is called tmux_conf for tmux.conf then the deployment
    path will be as follows:

    Deployment Path: config_repo/tmux_repo/tmux_conf/tmux.conf

    Note, that only the Deployment name is suffixed with "_repo" for
    clarification

    :param deployment_path: Path to the Deployment
    :param unit: Name of the Deployment Unit to create the path
    :return: None
    """
    u_path = deployment_path / unit
    u_path.mkdir(exist_ok=True)


def _set_config_repo(deployment: str) -> Path:
    """
    Create the repo path for each deployemtn
    :param deployment: Deployment name i.e. tmux
    :return:
    """
    d_path = CONFIG_REPO / f"{deployment}_repo"
    d_path.mkdir(exist_ok=True)
    return d_path


def _get_config() -> Optional[dict]:
    """
    Fetches the config file located at the relative fixed path to this script.
    If the file is not found, then an error will be thrown.
    :return: Dictionary containing the configuration for fetching dotfiles
    :rtype: dict
    """
    if not CONFIG_PATH.exists():
        exit(f"[!] There is no config file available at "
             f"{CONFIG_PATH.as_posix()}")

    with CONFIG_PATH.open("rt", encoding="utf-8") as handle:
        return json.load(handle)


def _get_args() -> argparse.Namespace:
    """
    Parse the command line arguments to ensure that the proper options were
    picked
    :return: Parse arguments Namespace
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser(
        description="Tool fetches all the configuration files specified in the"
                    " json file. The destination can be left to "
                    "None and a the script will automatically name the "
                    "destination folder."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--fetch_configs",
        help="Fetch all the configs specified in the json file",
        action="store_true",
        dest="fetch_configs",
        default=False
    )
    group.add_argument(
        "--deploy_configs",
        help="Deploy all the configs specified in the json file",
        action="store_true",
        dest="deploy_configs",
        default=False
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()

