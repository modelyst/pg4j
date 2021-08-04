import typer
from typing import List
from time import sleep
from pathlib import Path
from os import getcwd, listdir, environ, mkdir
from dataclasses import asdict
from .utils import (
    get_conn,
    dump_query,
    read_schema,
    parse_table,
    filters_to_filter_func,
    snake_to_camel,
)
from .classes import Table
from sqlalchemy import create_engine
import re

# DEFAULT Constants
ROOT_DIR = Path(getcwd())
SQL_DIR = ROOT_DIR / "sql"
OUTPUT_DIR = ROOT_DIR / "output"
USER = environ.get("USER", "postgres")
DEFAULT_DSN = f"postgres://{USER}:@localhost/camd"

app = typer.Typer()

DSN_OPTION = (
    typer.Option(
        DEFAULT_DSN, "--conn", "-c", help="Only run files that match this regex filter"
    ),
)
FILTERS_OPTION = typer.Option(
    [r".*"], "--filter", help="Only run files that match this regex filter"
)
COL_XCLUDE_FILTERS_OPTION = typer.Option(
    [], "--col-xclude", "-cx", help="Exclude columns that match these regex filters"
)
COL_INCLUDE_FILTERS_OPTION = typer.Option(
    [r".*"],
    "--col-include",
    "-ci",
    help="Only include columns that match these regex filters",
)
TAB_XCLUDE_FILTERS_OPTION = typer.Option(
    [],
    "--tab-xclude",
    "-tx",
    help="Exclude tables whose name matches these regex filters",
)
TAB_INCLUDE_FILTERS_OPTION = typer.Option(
    [r".*"],
    "--tab-include",
    "-ti",
    help="Include tables whose name matches these regex filters",
)


@app.command()
def dump(
    sql_folder: Path = typer.Option(
        SQL_DIR, "--sql", help="Folder to find nodes/ and edges/ sql files"
    ),
    output_folder: Path = typer.Option(
        OUTPUT_DIR, "--output", help="Folder to output results"
    ),
    sql_filters: List[str] = FILTERS_OPTION,
    dsn: str = DSN_OPTION,
):
    # Setup connection
    cxn = get_conn(dsn)
    patterns = [re.compile(sql_filter) for sql_filter in sql_filters]
    filter_func = lambda x: any(map(lambda pattern: pattern.match(x), patterns))
    try:
        # Iterate through nodes and edges
        for entity_type in ("nodes", "edges"):
            # Setup the directories to read from
            data_dir_curr = output_folder / entity_type
            sql_dir_curr = sql_folder / entity_type
            data_dir_curr.mkdir(parents=True, exist_ok=True)
            sql_paths = listdir(sql_dir_curr)
            # Iterate through paths and dump sql query to a csv
            basenames = list(
                filter(filter_func, map(lambda x: x.replace(".sql", ""), sql_paths))
            )
            typer.echo(basenames)
            with typer.progressbar(
                basenames,
                label=f"Getting {entity_type}",
                item_show_func=lambda x: f"{x}",
            ) as basenames_prog:
                for basename in basenames_prog:
                    sql_command = (
                        (sql_dir_curr / (basename + ".sql")).read_text().strip(";")
                    )
                    dump_query(
                        sql_command,
                        cxn,
                        data_dir_curr / f"{basename}.csv",
                    )
                    sleep(0.2)
    finally:
        cxn.close()


@app.command("map")
def mapper(
    dsn: str = DSN_OPTION,
    col_exclude_filters: List[str] = COL_XCLUDE_FILTERS_OPTION,
    col_include_filters: List[str] = COL_INCLUDE_FILTERS_OPTION,
    tab_exclude_filters: List[str] = TAB_XCLUDE_FILTERS_OPTION,
    tab_include_filters: List[str] = TAB_INCLUDE_FILTERS_OPTION,
):
    # Compile filter func
    col_include_filter_func = filters_to_filter_func(col_include_filters)
    col_exclude_filter_func = filters_to_filter_func(col_exclude_filters)
    tab_include_filter_func = filters_to_filter_func(tab_include_filters)
    tab_exclude_filter_func = filters_to_filter_func(tab_exclude_filters)

    engine = create_engine(dsn)
    metadata = read_schema(engine)
    col_map = {}
    node_sql_stmts = {}
    edge_sql_stmts = {}
    for full_table_name, table in metadata.tables.items():
        schema, table_name = full_table_name.split(".")
        if tab_include_filter_func(table_name) and not tab_exclude_filter_func(
            table_name
        ):
            tab = Table.from_sqlalchemy(table)

            tab_sql = tab.toSQL(
                metadata, col_include_filter_func, col_exclude_filter_func, col_map
            )

            if not tab.is_mapping_table(metadata):
                node_sql_stmts[f"{tab.name}.sql"] = tab_sql
                for fk in tab.foreign_keys:
                    edge_sql = fk.toSQL()
                    edge_sql_stmts[
                        f"{fk.source_table}__{fk.target_table}.sql"
                    ] = edge_sql
            else:
                edge_sql_stmts[f"{tab.name}.sql"] = tab_sql

    for name, stmts in zip(("nodes", "edges"), (node_sql_stmts, edge_sql_stmts)):
        directory = Path(f"./{name}")
        directory.mkdir(parents=True, exist_ok=True)
        for file_name, sql in stmts.items():
            with open(directory / file_name, "w") as f:
                f.write(str(sql))
