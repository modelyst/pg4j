from pathlib import Path
from typing import List, Dict

from sqlalchemy import create_engine

from .classes import Table
from .typer_options import (
    COL_INCLUDE_FILTERS_OPTION,
    COL_XCLUDE_FILTERS_OPTION,
    DSN_OPTION,
    TAB_INCLUDE_FILTERS_OPTION,
    TAB_XCLUDE_FILTERS_OPTION,
)
from .utils import filters_to_filter_func, read_schema


def mapper(
    dsn: str = DSN_OPTION,
    schema: str = "public",
    col_exclude_filters: List[str] = COL_XCLUDE_FILTERS_OPTION,
    col_include_filters: List[str] = COL_INCLUDE_FILTERS_OPTION,
    tab_exclude_filters: List[str] = TAB_XCLUDE_FILTERS_OPTION,
    tab_include_filters: List[str] = TAB_INCLUDE_FILTERS_OPTION,
    write: bool = False,
    ignore_mapping: bool = False
) -> Dict[str, Dict[str, str]]:
    # Compile filter func
    col_include_filter_func = filters_to_filter_func(col_include_filters)
    col_exclude_filter_func = filters_to_filter_func(col_exclude_filters)
    tab_include_filter_func = filters_to_filter_func(tab_include_filters)
    tab_exclude_filter_func = filters_to_filter_func(tab_exclude_filters)

    engine = create_engine(dsn)
    metadata = read_schema(engine, schema)
    col_map = {}
    node_sql_stmts = {}
    edge_sql_stmts = {}
    for full_table_name, table in metadata.tables.items():
        try:
            _, table_name = full_table_name.split(".")
        except ValueError:
            table_name = full_table_name

        if tab_include_filter_func(table_name) and not tab_exclude_filter_func(
            table_name
        ):
            tab = Table.from_sqlalchemy(table)
            tab_sql = tab.toSQL(
                metadata, col_include_filter_func, col_exclude_filter_func, col_map, ignore_mapping
            )

            if ignore_mapping or not tab.is_mapping_table(metadata):
                node_sql_stmts[f"{tab.name}.sql"] = tab_sql
                for fk in tab.foreign_keys:
                    if tab_include_filter_func(
                        fk.target_table
                    ) and not tab_exclude_filter_func(fk.target_table):
                        edge_sql = fk.toSQL()
                        edge_sql_stmts[
                            f"{fk.source_table}__{fk.target_table}.sql"
                        ] = edge_sql
            else:
                fk_1, fk_2 = tab.foreign_keys
                if (
                    tab_include_filter_func(fk_1.target_table)
                    and not tab_exclude_filter_func(fk_1.target_table)
                    and tab_include_filter_func(fk_2.target_table)
                    and not tab_exclude_filter_func(fk_2.target_table)
                ):
                    edge_sql_stmts[f"{tab.name}.sql"] = tab_sql

    if write:
        for name, stmts in zip(("nodes", "edges"), (node_sql_stmts, edge_sql_stmts)):
            directory = Path(f"./{name}")
            directory.mkdir(parents=True, exist_ok=True)
            for file_name, sql in stmts.items():
                with open(directory / file_name, "w") as f:
                    f.write(str(sql))

    return {"nodes": node_sql_stmts, "edges": edge_sql_stmts}
