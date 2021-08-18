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

from pathlib import Path
from shutil import rmtree
from time import sleep
from typing import Dict, List

import typer

from pg4j.cli.typer_options import (
    COL_INCLUDE_FILTERS_OPTION,
    COL_XCLUDE_FILTERS_OPTION,
    CONFIG_OPTION,
    DSN_OPTION,
    TAB_INCLUDE_FILTERS_OPTION,
    TAB_XCLUDE_FILTERS_OPTION,
    VERSION_OPTION,
)
from pg4j.config import Pg4jConfig
from pg4j.mapper import mapper
from pg4j.sql import dump_query, get_conn, parse_dsn

# DEFAULTS
ROOT_DIR = Path.cwd()
SQL_DIR = ROOT_DIR / "sql"
OUTPUT_DIR = ROOT_DIR / "output"


def dump(
    sql_folder: Path = typer.Option(SQL_DIR, "--sql", help="Folder to find nodes/ and edges/ sql files"),
    output_folder: Path = typer.Option(OUTPUT_DIR, "--output", help="Folder to output results"),
    schema: str = "public",
    col_exclude_filters: List[str] = COL_XCLUDE_FILTERS_OPTION,
    col_include_filters: List[str] = COL_INCLUDE_FILTERS_OPTION,
    tab_exclude_filters: List[str] = TAB_XCLUDE_FILTERS_OPTION,
    tab_include_filters: List[str] = TAB_INCLUDE_FILTERS_OPTION,
    dsn: str = DSN_OPTION,
    db_password: str = typer.Option("", "--password", "-p"),
    ignore_mapping: bool = typer.Option(False, "--ignore-auto-mapping"),
    read: bool = False,
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite the output_folder"),
    config_file: Path = CONFIG_OPTION,
    version: bool = VERSION_OPTION,
):
    config = Pg4jConfig.from_yaml(config_file)

    # Setup connection
    parsed_dsn = parse_dsn(dsn)
    if not db_password and "password" not in parsed_dsn:
        db_password = typer.prompt("Please Enter DB Password", "")
    engine = get_conn(dsn, db_password)
    sql_stmts: Dict[str, Dict[str, str]] = {"nodes": {}, "edges": {}}
    if overwrite:
        if output_folder.exists():
            rmtree(output_folder)
        output_folder.mkdir()
    if read:
        for entity_type in ("nodes", "edges"):
            # Setup the directories to read from
            sql_dir_curr = sql_folder / entity_type

            sql_paths = [file_name for file_name in sql_dir_curr.iterdir() if file_name.suffix == ".sql"]
            for basename in sql_paths:
                sql_command = basename.read_text().strip().strip(";")
                sql_stmts[entity_type][basename.name] = sql_command

    else:
        sql_stmts = mapper(
            dsn,
            schema,
            col_exclude_filters,
            col_include_filters,
            tab_exclude_filters,
            tab_include_filters,
            engine=engine,
            ignore_mapping=ignore_mapping,
            config=config,
        )

    try:
        # Iterate through nodes and edges
        for entity_type in ("nodes", "edges"):
            data_dir_curr = output_folder / entity_type
            data_dir_curr.mkdir(parents=True, exist_ok=True)
            for file_name, sql_command in sql_stmts[entity_type].items():
                dump_query(
                    sql_command,
                    engine,
                    data_dir_curr / file_name.replace(".sql", ".csv"),
                )
                sleep(0.2)
    finally:
        engine.dispose()
