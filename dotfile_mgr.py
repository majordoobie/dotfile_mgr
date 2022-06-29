import argparse
import filecmp
import importlib.util
import json
import pathlib
import shutil
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import List, Optional
from itertools import groupby

SELF_PATH = Path(__file__).parents[0]
CONFIG_REPO = SELF_PATH / "config_repo"
CONFIG_PATH = CONFIG_REPO
JSON_FILE = "dotfiles.json"
YAML_FILES = ["dotfiles.yml", "dotfiles.yaml"]
YAML_MODULE = "yaml"

# Set the mandatory dict keys
ROOT_JSON = "dotfiles"
DEPLOYMENT_K = "deployment_fpath"
STORAGE_FPATH_K = "storage_fpath"
STORAGE_PATH_K = "storage_path"
STORAGE_PREFIX = "${S_ROOT}"


class ConfigType(Enum):
    """Used to denote what configuration type is used"""
    JSON = auto()
    YAML = auto()


@dataclass
class DeploymentObject:
    deployment_unit: str
    deployment_obj: str
    deployment_path: Path
    storage_path: str
    storage_path_used: bool

    valid: bool = False
    _storage_path: Path = None

    @property
    def get_storage_name(self) -> str:
        """
        If the prefix is used, then return a shorter string so that
        the terminal output is cleaner. If it's a full path, then keep the
        full string.
        :return:
        """
        if self.storage_path_used:
            return self._storage_path.relative_to(SELF_PATH).as_posix()
        else:
            return self._storage_path.as_posix()

    def __post_init__(self) -> None:
        """
        Expand the storage string to a Path object by interpreting if
        the configuration is using either a literal path, D_ROOT path,
        or D_ROOT file.

        Literal Path:
            The literal path is a path that does not use the {D_ROOT} prefix
            meaning that the DeploymentObject will not attempt to place the
            file in the directory that it has created for it. Instead,
            the DO will use the full path used by the configuration
            wherever that may be

            Example: /full/path/to/storage/can/be/anywhere

        D_ROOT Path:
            D_ROOT Path will use the D_ROOT directory plus create any
            subdirectories specified and copy the source file to this
            directory with the exact same name.

        D_ROOT File:
            D_ROOT File is just like D_ROOT Path where it will make
            all the directories if anywhere added but it will assume
            that the last "directory" is the name of the target file.
        :return:
        """
        # Check if config calls for using the storage directory
        if self.storage_path.startswith(STORAGE_PREFIX):

            # Create the base directory for this deployment obj
            self._storage_path = CONFIG_REPO / self.deployment_unit

            # Now append the reset of the path
            path_string = self.storage_path.lstrip(STORAGE_PREFIX)
            self._storage_path = self._storage_path / path_string

            # If storage path, just mkdir, else we need to strip, then mkdir
            if self.storage_path:
                self._storage_path.mkdir(parents=True, exist_ok=True)
            else:
                # This will mkdir everything except the filename
                self._storage_path.parents[0].mkdir(parents=True,
                                                    exist_ok=True)
        else:
            self._storage_path = Path(self.storage_path)

        # Expand the deployment path incase the tilda was used
        self.deployment_path = self.deployment_path.expanduser()

    def deploy_config(self) -> None:
        if not self._storage_path.exists():
            print(f"[+] The storage path {self.deployment_obj}@"
                  f"{self._storage_path.as_posix()} does not exist. "
                  f"\nSkipping...")
            return

        # Check if the deployment path exists, if it does not
        # pop the file name and check if that directory exists.
        # If it does not, create it.
        file_exists = True
        if not self.deployment_path.exists():
            file_exists = False
            deployment_dir = self.deployment_path.parents[0]
            if not deployment_dir.exists():
                try:
                    deployment_dir.mkdir(parents=True)
                except Exception as error:
                    print(error)
                    return

        # If storage_path is a dir, get the file
        if self.storage_path_used:
            storage_file = self._storage_path / self.deployment_path.name
        else:
            storage_file = self._storage_path

        # Ensure that storage path exists
        if not storage_file.exists():
            print(f"[!] Storage file {self.deployment_obj}@"
                  f"{storage_file} does not exist")
            return

        # Check that the contents have not change, if they have
        # then go ahead and copy. The filecmp does a byte byte
        # comparison instead of a hash
        do_copy = True
        if file_exists:
            if filecmp.cmp(self.deployment_path, storage_file):
                do_copy = False
                print(f"[-] [{self.deployment_unit}] already up to date: "
                      f"{self.deployment_path.name}")

        if do_copy:
            try:
                print(
                    f"[+] [{self.deployment_unit}] "
                    f"{self.get_storage_name} -> "
                    f"{self.deployment_path}")
                shutil.copy(storage_file, self.deployment_path)
            except Exception as error:
                print(error)

    def fetch_config(self) -> None:
        """
        Determine that the deployment path exists before attempting to copy
        from that path to the storage folder.

        If the storage path already exists, then determine that the files
        are different before attempting to copy them over.
        """
        if not self.deployment_path.exists():
            print(f"[!] The deployment path {self.deployment_obj}@"
                  f"{self.deployment_path.as_posix()} does not exist")
            return

        # Check if the destination file exist, if it does check if
        # the contents are different using the byte to byte comparison
        do_copy = True
        if (self._storage_path / self.deployment_path.name).exists():
            # If files are the same, do not copy
            if filecmp.cmp(self.deployment_path,
                           (self._storage_path / self.deployment_path.name)):
                do_copy = False
                print(f"[-] [{self.deployment_unit}] Already up to "
                      f"date: {self.deployment_path.name}")

        if do_copy:
            try:
                print(
                    f"[+] [{self.deployment_unit}] {self.deployment_path} -> "
                    f"{self.get_storage_name}")
                shutil.copy(self.deployment_path, self._storage_path)
            except FileNotFoundError as error:
                print(error)
            except Exception as error:
                print(error)


def _create_config(directory: pathlib.Path, d_unit_name: str) -> None:
    # Expand if they are using tilda
    directory = directory.expanduser()

    # If not a directory, exit
    if not directory.is_dir():
        exit("Path passed is not a directory")

    # Glob the directory for all the files that are actual files
    files = \
        sorted(
            list(
                map(
                    lambda x: '~' / x.relative_to(Path.home()),
                    filter(
                        lambda x: x.is_file(),
                        directory.glob("**/*")
                    )
                )
            ),
            key=lambda x: x.name
        )

    # Calculate if any of the config files are duplicates, if so, change their
    # name to avoid duplicate to avoid duplicate deployment object names
    dupe_dict = {}
    for dupe, count in groupby(files, key=lambda x: x.name):
        count = len(list(count))
        if count > 1:
            dupe_dict[dupe] = count

    # Printout the config made
    config = f"  {d_unit_name}:\n"
    for deploy_obj in files:
        d_name = deploy_obj.stem
        if dupe_dict.get(deploy_obj.name) and dupe_dict.get(deploy_obj.name) > 0:
            d_name = f"{d_name}_{dupe_dict.get(deploy_obj.name)}"
            dupe_dict[deploy_obj.name] -= 1

        config += (
              f"    - {d_name}:\n"
              f"        deployment_fpath: {deploy_obj}\n"
              f"        storage_path: {STORAGE_PREFIX}\n")
    print(config)


def main():
    # Get command line arguments
    args = _get_args()

    if args.create_config:
        _create_config(args.create_config, "NeoVim")
        exit()

    # Parse the config to make sure that it is a valid json
    try:
        config_file = _get_config(None)
    except ValueError as error:
        exit(error)

    # Get list of deployment objects
    deployments = _get_deployments(config_file)

    # If fetch
    if args.fetch_configs:
        for deployment in deployments:
            deployment.fetch_config()

    elif args.deploy_configs:
        for deployment in deployments:
            deployment.deploy_config()


def _get_config_file() -> dict:
    """
    Function attempts to iterate over the possible configuration
    file names. If no matches are found, raise an exception.
    :return:
    """
    paths = (
        (ConfigType.JSON, CONFIG_PATH / JSON_FILE),
        (ConfigType.YAML, CONFIG_PATH / YAML_FILES[0]),
        (ConfigType.YAML, CONFIG_PATH / YAML_FILES[1])
    )
    for path in paths:
        if path[1].exists():
            try:
                with path[1].open("rt", encoding="utf-8") as handle:
                    if path[0] == ConfigType.JSON:
                        return json.load(handle)
                    else:
                        # Check if the YAML module exists before importing
                        if importlib.util.find_spec(YAML_MODULE) is not None:
                            import yaml
                            return yaml.safe_load(handle)
                        else:
                            raise ModuleNotFoundError(
                                f"[!] Found yaml config file but could not "
                                f"import the PyYAML module. Please install the"
                                f" module using the requirements.txt file"
                            )
            except Exception as error:
                exit(error)

    # If no files can be found, then exit
    raise FileNotFoundError(f"[!] There is no config file available at "
                            f"{CONFIG_PATH.as_posix()}")


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
        config = _get_config_file()

    # First test if the root key is present. If it is not, exit
    if not config.get(ROOT_JSON):
        raise ValueError(
            "[!] INVALID JSON FORMAT: dotfiles.json missing root key "
            f"\"{ROOT_JSON}\" located at {CONFIG_PATH.as_posix()}")

    # Next, iterate over the dict and check that each deployment unit
    # has at least 1 deployment object where each deployment object
    # has at most two keys, being "DEPLOYMENT" and "STORAGE"
    for deployment_unit in config[ROOT_JSON].keys():

        # First test if deployment_unit is a LIST
        if not isinstance(config[ROOT_JSON][deployment_unit], list):
            raise ValueError(
                f"[!] [{deployment_unit}] does not contain a list of "
                f"deployment objects")

        # Check that each deployment unit has at least one deployment object
        if not config[ROOT_JSON][deployment_unit]:
            raise ValueError(
                f"[!] Deployment unit {deployment_unit} is empty!")

        # If list check that each deployment unit only has two keys,
        # DEPLOYMENT_K and STORAGE_K
        for deployment_obj in config[ROOT_JSON][deployment_unit]:
            for obj_name, obj_paths in deployment_obj.items():

                # First check that there is only two keys
                if len(obj_paths.keys()) != 2:
                    raise ValueError(
                        f"[!] Deployment obj {obj_name} contains "
                        f"more than two keys. Only "
                        f"{DEPLOYMENT_K}, {STORAGE_PATH_K}, "
                        f"{STORAGE_FPATH_K} can be used")

                # Check for the two mandatory keys
                if obj_paths.get(DEPLOYMENT_K) is None:
                    raise ValueError(
                        f"[!] {obj_name} is missing required key "
                        f"{DEPLOYMENT_K}")

                if obj_paths.get(STORAGE_PATH_K) is None and obj_paths.get(
                        STORAGE_FPATH_K) is None:
                    raise ValueError(
                        f"[!] {obj_name} is missing required key "
                        f"{STORAGE_FPATH_K} or {STORAGE_PATH_K}")
    return config


def _get_deployments(config: dict) -> List[DeploymentObject]:
    """
    Parse through the dict object and return a list of deployment objects.
    Each deployment object will have the deployment path and the source
    path.

    :param config: Dictionary containing the dotfile configuration paths
    :return: List of deployment objects
    """
    deployments = []
    for deployment_unit in config[ROOT_JSON].keys():
        for deployment_obj in config[ROOT_JSON][deployment_unit]:
            for obj_name, obj_paths in deployment_obj.items():
                # Check if storage path was used for the DO constructor
                storage_path_used = True if obj_paths.get(
                    STORAGE_PATH_K) else False

                # Storage string
                storage_string = obj_paths.get(STORAGE_PATH_K) \
                    if obj_paths.get(STORAGE_PATH_K) \
                    else obj_paths.get(STORAGE_FPATH_K)

                # Append a new DO object to the deployments list
                deployments.append(DeploymentObject(
                    deployment_unit,
                    obj_name,
                    Path(obj_paths.get(DEPLOYMENT_K)),
                    storage_string,
                    storage_path_used
                )
                )
    return deployments


def _get_args() -> argparse.Namespace:
    """
    Parse the command line arguments to ensure that the proper options were
    picked
    :return: Parse arguments Namespace
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser(
        description=("%(prog)s manages your dotfiles by fetching "
                     "and deploying them based on the paths set up "
                     "in the %(prog)s config. To use this tool, you "
                     "will need a configuration file in either json or"
                     "yaml format. The configuration format can be found "
                     "the git repo.")
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--fetch_configs",
        help="Fetch config files specified in the %(prog)s config",
        action="store_true",
        dest="fetch_configs",
        default=False
    )
    group.add_argument(
        "--deploy_configs",
        help="Deploy config files specified in the %(prog)s config",
        action="store_true",
        dest="deploy_configs",
        default=False
    )
    group.add_argument(
        "--create_config",
        help="Help create a deployment unit by globbing the directory "
             "specified",
        dest="create_config",
        type=pathlib.Path,
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
