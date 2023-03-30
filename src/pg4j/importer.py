#   Copyright 2021 Modelyst LLC
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import shutil
import subprocess
from enum import Enum
from pathlib import Path
from typing import List, Tuple

import typer

from pg4j.cli.styles import bad_typer_print, delimiter, good_typer_print, theme_typer_print
from pg4j.cli.typer_options import (
    FILE_INCLUDE_FILTERS_OPTION,
    NEO4J_HOME_OPTION,
    PG4J_DATA_DIR_OPTION,
    VERSION_OPTION,
)
from pg4j.inputs import DataDirectory, Pg4jImport
from pg4j.utils import filters_to_filter_func

bad_delimiter = lambda: delimiter(typer.colors.RED)


class ID_TYPE(Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    ACTUAL = "ACTUAL"


def importer(
    data_dirs: List[Path] = PG4J_DATA_DIR_OPTION,
    include_regex: List[str] = FILE_INCLUDE_FILTERS_OPTION,
    neo4j_path: Path = NEO4J_HOME_OPTION,
    admin_command: str = typer.Option("neo4j-admin", "--command", help="neo4j-admin command"),
    dbname: str = typer.Option("neo4j", "--dbname", "-d", help="Neo4j Database to import into"),
    id_type: ID_TYPE = typer.Option("STRING", "--id-type", help="Type of the imported node ids"),
    import_path: Path = typer.Option(
        None, "--import-file", help="Input file indicating the directories to be imported"
    ),
    quiet: bool = typer.Option(False, "-q", help="Suppress most output messages except errors"),
    overwrite: bool = False,
    _: bool = VERSION_OPTION,
):
    """
    Import data_directory into neo4j instance.
    """
    imports = Pg4jImport.from_yaml(import_path)
    include_filter = filters_to_filter_func(set(include_regex))

    # Check if neo4j is running and quit if found
    running, stop_command = check_neo4j_running()
    if running:
        bad_typer_print(
            "Detected neo4j is running.\n"
            "Please turn off the instance before running the import.\n"
            f"Try `{stop_command}` (sudo may be required)."
        )
        raise typer.Exit(code=2)

    # Build the neo4j-admin import command by reading the data_dirs and adding additional labels
    import_cmd = [
        f"{admin_command}",
        "database",
        "import",
        "full",
        dbname,
        f"--id-type={id_type.value}",
        "--skip-duplicate-nodes",
        f"--overwrite-destination=true",
    ]
    subfolders = ["nodes", "edges"]
    neo4j_types = ["nodes", "relationships"]
    config_dirs = imports.data_dirs
    data_dir_set = set(data_dirs + list(config_dirs.keys()))
    for data_dir in data_dir_set:
        added_labels = config_dirs.get(data_dir, DataDirectory()).labels
        joined_labels = ":".join(added_labels)
        added_label_str = f"={joined_labels}" if joined_labels else ""

        for subfolder, neo4j_type in zip(subfolders, neo4j_types):
            csv_folder = Path(data_dir) / subfolder
            for fname in csv_folder.iterdir():
                if fname.stat().st_size <= 10:
                    print(f"Skipping {fname} as it appears empty...")
                    continue
                fname_str = str(fname)
                assert fname_str.endswith(".csv")
                if include_filter(str(fname.name)):
                    import_cmd.append(f"--{neo4j_type}{added_label_str}={fname}")
                else:
                    theme_typer_print(f"Excluding {fname.name} due to filter")

    if not quiet:
        theme_typer_print("Running following import command:")
        theme_typer_print(" \\\n".join(import_cmd))
        delimiter()

    # Remove database in Neo4j instance if it previously existed and --overwrite set
    for file_name in ("databases", "transactions"):
        pth = neo4j_path / "data" / file_name / dbname
        if pth.exists():
            if overwrite:
                shutil.rmtree(pth)
            else:
                raise typer.BadParameter(f"{pth} already exists need to run with --overwrite to overwrite")

    # Run import command
    process = subprocess.Popen(import_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = process.stdout.readline() if process.stdout else b""
        if process.poll() is not None:
            break
        if output and not quiet:
            theme_typer_print(output.decode().strip())

    # Check return value on import to see if it failed and, if so, print error
    retval = process.poll()
    if retval != 0:
        bad_delimiter()
        if process.stderr:
            stderr = process.stderr.read().decode().strip()
            bad_typer_print("Encountered error during import:")
            bad_delimiter()
            bad_typer_print(stderr)
        else:
            bad_typer_print("Encountered unknown error during import...")
        bad_delimiter()
        raise typer.Exit(code=2)

    # Print success message
    if not quiet:
        delimiter()
        good_typer_print(
            "Finished! Restart your neo4j instance using a command like `sudo neo4j start` or `sudo systemctl start neo4j`"
        )


def check_neo4j_running() -> Tuple[bool, str]:
    """Run shell commands to see if the neo4j instance is running.py

    Returns:
        Tuple[bool, str]: First value is boolean indicating if neo4j is running, second is a suggested stop command
    """
    neo4j_status_check = lambda x: x.startswith("Neo4j is running")
    service_check = lambda x: "Active: active (running)" in x
    check_commands = (
        (["neo4j", "status"], neo4j_status_check, "neo4j stop"),
        (["service", "neo4j", "status"], service_check, "systemctl stop neo4j"),
        (["systemctl", "neo4j", "status"], service_check, "systemctl stop neo4j"),
    )
    for check_command, running_func, stop_cmd in check_commands:
        try:
            proc = subprocess.Popen(check_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.wait()
            (stdout, _) = proc.communicate()
            stdout_str = stdout.decode().strip()
            if running_func(stdout_str):
                return True, stop_cmd
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    return False, ""
