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
from pathlib import Path
from typing import List

from pg4j.cli.typer_options import (
    CONFIG_OPTION,
    FILE_INCLUDE_FILTERS_OPTION,
    NEO4J_HOME_OPTION,
    PG4J_DATA_DIR_OPTION,
    VERSION_OPTION,
)
from pg4j.config import DataDirectory, Pg4jConfig
from pg4j.utils import filters_to_filter_func


def importer(
    data_dirs: List[Path] = PG4J_DATA_DIR_OPTION,
    include_regex: List[str] = FILE_INCLUDE_FILTERS_OPTION,
    neo4j_path: Path = NEO4J_HOME_OPTION,
    dbname: str = "neo4j",
    config_path: Path = CONFIG_OPTION,
    start_neo4j: bool = True,
    overwrite: bool = False,
    version: bool = VERSION_OPTION,
):
    """
    Import data_directory into neo4j instance.
    """
    config = Pg4jConfig.from_yaml(config_path)
    include_filter = filters_to_filter_func(include_regex)

    neo4j_stop_cmd = ["neo4j", "stop"]
    import_cmd = [
        "neo4j-admin",
        "import",
        "--id-type=STRING",
        "--skip-duplicate-nodes",
        f"--database={dbname}",
    ]
    subfolders = ["nodes", "edges"]
    neo4j_types = ["nodes", "relationships"]
    config_dirs = config.data_dirs
    data_dir_set = set(data_dirs + list(config_dirs.keys()))
    for data_dir in data_dir_set:
        added_labels = config_dirs.get(data_dir, DataDirectory()).labels
        joined_labels = ":".join(added_labels)
        added_label_str = f"={joined_labels}" if joined_labels else ""

        for subfolder, neo4j_type in zip(subfolders, neo4j_types):
            csv_folder = Path(data_dir) / subfolder
            for fname in csv_folder.iterdir():
                fname_str = str(fname)
                assert fname_str.endswith(".csv")
                if include_filter(str(fname.name)):
                    import_cmd.append(f"--{neo4j_type}{added_label_str}={fname}")
                else:
                    print(f"Excluding {fname.name} due to filter")

    neo4j_start_cmd = ["neo4j", "start"]
    print("\n".join(import_cmd))

    print("######")
    output = subprocess.check_output(neo4j_stop_cmd)
    print(output.decode().strip())
    print("######")
    for file_name in ("databases", "transactions"):
        pth = neo4j_path / file_name / dbname
        if pth.exists():
            if overwrite:
                shutil.rmtree(pth)
            else:
                raise
    import_output = subprocess.check_output(import_cmd)
    print(import_output.decode().strip())
    print("######")
    if start_neo4j:
        output = subprocess.check_output(neo4j_start_cmd)
        print(output.decode().strip())
    print("######")
    print("Finished")
