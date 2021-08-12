from pathlib import Path
from time import sleep
from typing import List
import typer
from shutil import rmtree
from .typer_options import (
    DSN_OPTION,
    COL_XCLUDE_FILTERS_OPTION,
    COL_INCLUDE_FILTERS_OPTION,
    TAB_XCLUDE_FILTERS_OPTION,
    TAB_INCLUDE_FILTERS_OPTION,
)
from .utils import dump_query, get_conn
from .mapper import mapper

# DEFAULTS
ROOT_DIR = Path.cwd()
SQL_DIR = ROOT_DIR / "sql"
OUTPUT_DIR = ROOT_DIR / "output"


def dump(
    sql_folder: Path = typer.Option(
        SQL_DIR, "--sql", help="Folder to find nodes/ and edges/ sql files"
    ),
    output_folder: Path = typer.Option(
        OUTPUT_DIR, "--output", help="Folder to output results"
    ),
    schema: str = "public",
    col_exclude_filters: List[str] = COL_XCLUDE_FILTERS_OPTION,
    col_include_filters: List[str] = COL_INCLUDE_FILTERS_OPTION,
    tab_exclude_filters: List[str] = TAB_XCLUDE_FILTERS_OPTION,
    tab_include_filters: List[str] = TAB_INCLUDE_FILTERS_OPTION,
    dsn: str = DSN_OPTION,
    db_password: str = typer.Option(
        None, prompt=True, confirmation_prompt=True, hide_input=True
    ),
    ignore_mapping: bool = typer.Option(False, "--ignore-auto-mapping"),
    read: bool = False,
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Overwrite the output_folder"
    ),
):
    # Setup connection
    engine = get_conn(dsn, db_password)
    sql_stmts = {"nodes": {}, "edges": {}}
    if overwrite:
        rmtree(output_folder)
        output_folder.mkdir()
    if read:
        for entity_type in ("nodes", "edges"):
            # Setup the directories to read from
            sql_dir_curr = sql_folder / entity_type

            sql_paths = [
                file_name
                for file_name in sql_dir_curr.iterdir()
                if file_name.suffix == ".sql"
            ]
            for basename in sql_paths:
                sql_command = basename.read_text().strip(";")
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
