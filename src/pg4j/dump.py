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
from pydantic import SecretStr

from pg4j.cli.typer_options import (
    COL_INCLUDE_FILTERS_OPTION,
    COL_XCLUDE_FILTERS_OPTION,
    DSN_OPTION,
    SETTINGS_OPTION,
    TAB_INCLUDE_FILTERS_OPTION,
    TAB_XCLUDE_FILTERS_OPTION,
    VERSION_OPTION,
)
from pg4j.inputs import Pg4jMapping
from pg4j.mapper import mapper
from pg4j.settings import Pg4jSettings
from pg4j.sql import dump_query, get_conn

# DEFAULTS
ROOT_DIR = Path.cwd()
SQL_DIR = ROOT_DIR / "sql"
OUTPUT_DIR = ROOT_DIR / "output"


def dump(
    sql_folder: Path = typer.Option(SQL_DIR, "--sql", help="Folder to find nodes/ and edges/ sql files"),
    output_folder: Path = typer.Option(OUTPUT_DIR, "--output", help="Folder to output results"),
    col_exclude_filters: List[str] = COL_XCLUDE_FILTERS_OPTION,
    col_include_filters: List[str] = COL_INCLUDE_FILTERS_OPTION,
    tab_exclude_filters: List[str] = TAB_XCLUDE_FILTERS_OPTION,
    tab_include_filters: List[str] = TAB_INCLUDE_FILTERS_OPTION,
    postgres_dsn: str = DSN_OPTION,
    postgres_password: str = typer.Option(None, "--password", "-p", envvar="PG4J__POSTGRES_PASSWORD"),
    postgres_schema: str = typer.Option(
        None, "--schema", help="Schema in the postgres db to dump from.", envvar="PG4J__POSTGRES_SCHEMA"
    ),
    settings_file: Path = SETTINGS_OPTION,
    use_mapper: bool = typer.Option(True, "--map", help="Map the existing schema using the pg4j mapper."),
    ignore_mapping: bool = typer.Option(False, "--ignore-auto-mapping"),
    mapping_input: Path = None,
    read: bool = False,
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite the output_folder"),
    _: bool = VERSION_OPTION,
):

    # Set the settings overriding with cli args
    override_settings = {
        "postgres_dsn": postgres_dsn,
        "postgres_password": postgres_password,
        "postgres_schema": postgres_schema,
    }
    override_settings = {key: val for key, val in override_settings.items() if val is not None}
    settings = Pg4jSettings(_env_file=settings_file, **override_settings)  # type: ignore
    # Setup connection
    # if password not provided in the DSN or postgres_password field prompt the user
    if not (settings.postgres_dsn.password or settings.postgres_password.get_secret_value()):
        settings.postgres_password = SecretStr(typer.prompt("Please Enter DB Password", ""))

    engine = get_conn(settings.postgres_dsn, settings.postgres_password.get_secret_value())

    # Check the output folder for existence and remove it or raise error
    if output_folder.exists():
        if overwrite:
            rmtree(output_folder)
        else:
            raise typer.BadParameter(
                f"Output folder {output_folder} already exists. Please remove the folder or use the --overwrite flag."
            )
    # initialize output folder for data dump
    output_folder.mkdir()

    # Setup the sql statements as dict of dict
    sql_stmts: Dict[str, Dict[str, str]] = {"nodes": {}, "edges": {}}

    # If reading read the local sql_dir for the statements to run against the DB
    if read:
        for entity_type in ("nodes", "edges"):
            # Setup the directories to read from
            sql_dir_curr = sql_folder / entity_type

            sql_paths = [file_name for file_name in sql_dir_curr.iterdir() if file_name.suffix == ".sql"]
            for basename in sql_paths:
                sql_command = basename.read_text().strip().strip(";")
                sql_stmts[entity_type][basename.name] = sql_command

    # If using mapper get the sql statements by mapping the metadata from the engine
    if use_mapper:
        mapping = Pg4jMapping.from_yaml(mapping_input) if mapping_input else Pg4jMapping()
        sql_stmts = mapper(
            mapping=mapping,
            schema=settings.postgres_schema,
            col_exclude_filters=set(col_exclude_filters),
            col_include_filters=set(col_include_filters),
            tab_exclude_filters=set(tab_exclude_filters),
            tab_include_filters=set(tab_include_filters),
            engine=engine,
            ignore_mapping=ignore_mapping,
        )

    # Run the sql_stmts against the database and write the results to local CSVs
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
