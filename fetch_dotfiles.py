import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

# Set paths to static files/folder
SELF_PATH = Path(__file__).parents[0]
CONFIG_REPO = SELF_PATH / "config_repo"
CONFIG_PATH = CONFIG_REPO / "dotfiles.json"

# Set the mandatory dict keys
ROOT_JSON = "dotfiles"
DEPLOYMENT_K = "deployment"
STORAGE_K = "storage"


@dataclass
class Deployment:
    deployment_name: str
    deployment_path: Path
    storage_path: Optional[Path]
    valid: bool = False


def main():
    # Get command line arguments
    args = _get_args()

    # Parse the config to make sure that it is a valid json
    config_file = _get_config()

    # Get list of deployment objects
    deployments = _get_deployments(config_file)


def _get_config(config: Optional[dict]) -> dict:
    """
    Iterate over the json file to first ensure that the file is VALID.
    A valid configuration is one that has the root key of `ROOT_JSON`
    and has at least one `deployment unit` where each `deployment unit`
    is a list of `deployment objects` each containing at most two keys,
    the `deployment` path and `storage` path.

    :return: Dictionary containing the configuration for fetching dotfiles
    :rtype: dict
    """
    if config is None:
        if not CONFIG_PATH.exists():
            exit(f"[!] There is no config file available at "
                 f"{CONFIG_PATH.as_posix()}")

        # read the config json into a dictionary
        with CONFIG_PATH.open("rt", encoding="utf-8") as handle:
            config = json.load(handle)

    # First test if the root key is present. If it is not, exit
    if not config.get(ROOT_JSON):
        exit("[!] INVALID JSON FORMAT: dotfiles.json missing root key "
             f"\"{ROOT_JSON}\" located at {CONFIG_PATH.as_posix()}")

    # Next, iterate over the dict and check that each deployment unit
    # has at least 1 deployment object where each deployment object
    # has at most two keys, being "DEPLOYMENT" and "STORAGE"
    for deployment_unit in config[ROOT_JSON].keys():
        # First test if deployment_unit is a LIST
        if not isinstance(config[ROOT_JSON][deployment_unit], list):
            exit(f"[!] {deployment_unit} does not contain a list of "
                 f"deployment objects")

        # Check that each deployment unit has at least one deployment object
        if not config[ROOT_JSON][deployment_unit]:
            exit(f"[!] Deployment unit {deployment_unit} is empty!")

        # If list, check that each deployment unit only has two keys,
        # DEPLOYMENT_K and STORAGE_K
        for deployment_obj in config[ROOT_JSON][deployment_unit]:
            for obj_name, obj_paths in deployment_obj.items():
                # First check that there is only two keys
                if len(obj_paths.keys()) != 2:
                    exit(f"[!] Deployment obj {deployment_obj} contains"
                         f"more than two keys")

                # Check for the two mandatory keys
                if obj_paths.get(DEPLOYMENT_K) is None:
                    exit(f"[!] {deployment_obj} is missing required key"
                         f"{DEPLOYMENT_K}")
                if obj_paths.get(STORAGE_K) is None:
                    exit(f"[!] {deployment_obj} is missing required key"
                         f"{STORAGE_K}")
    return config


def _get_deployments(config: dict) -> List[Deployment]:
    deployments = []
    for deployment_unit in config[ROOT_JSON].keys():
        for deployment_obj in config[ROOT_JSON][deployment_unit]:
            for obj_name, obj_paths in deployment_obj.items():
                deployments.append(Deployment(
                        obj_name,
                        obj_paths.get(DEPLOYMENT_K),
                        obj_paths.get(STORAGE_K)
                    )
                )
    return deployments


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

