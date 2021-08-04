from typing import List, Callable
from dataclasses import asdict
from pathlib import Path
from sqlalchemy import create_engine, text, MetaData, Table, ForeignKey as SAForeignKey
from sqlalchemy.engine import Engine
import re
from .classes import ForeignKey

FILTER_FUNC_TYPE = Callable[[str], bool]


def get_conn(dsn: str):
    engine = create_engine(dsn)
    engine.connect()


def snake_to_camel(string: str, first_capital: bool = False):
    first, *after = string.split("_")
    output = first.capitalize() if first_capital else first
    return output + "".join(map(lambda x: x.capitalize(), after))


def read_schema(engine: Engine):
    metadata = MetaData()
    metadata.reflect(bind=engine, schema="development")
    return metadata


def parse_table(
    table: Table,
    exclude_filter_func: FILTER_FUNC_TYPE,
    include_filter_func: FILTER_FUNC_TYPE,
) -> dict:
    primary_keys = [key.name for key in table.primary_key]
    if len(primary_keys) > 1:
        raise NotImplementedError("Haven't dealt with composite keys yet")
    primary_key = list(table.primary_key)[0]
    basic_cols = [
        col
        for col in table.columns
        if not col.primary_key
        and not col.foreign_keys
        and include_filter_func(col.name)
        and not exclude_filter_func(col.name)
    ]
    foreign_keys = [
        parse_foreign_key(list(col.foreign_keys)[0])
        for col in table.columns
        if col.foreign_keys
    ]
    mapping_table = len(foreign_keys) == 2
    print(f"Table Name: {table.name}")
    print(f"Foriegn Keys: {foreign_keys}")
    print(f"Cols: {basic_cols}")
    print(f"Mapping Table: {mapping_table}")
    print("######")


def parse_foreign_key(foreign_key: SAForeignKey) -> ForeignKey:
    target_column = foreign_key.column
    target_table = target_column.table
    source_column = foreign_key.parent
    source_table = source_column.table
    fk = ForeignKey(
        source_table.name, source_column.name, target_table.name, target_column.name
    )
    return fk


def dump_query(query: str, conn, path: Path):
    # set up our database connection.
    db_cursor = conn.cursor()

    # Use the COPY function on the SQL we created above.
    SQL_for_file_output = f"COPY ({query}) TO STDOUT WITH CSV HEADER"

    # Set up a variable to store our file path and name.
    with open(path, "w") as f_output:
        db_cursor.copy_expert(text(SQL_for_file_output), f_output)


def filters_to_filter_func(list_of_filters: List[str]) -> FILTER_FUNC_TYPE:
    # Compile filter func
    patterns = [re.compile(filter_str) for filter_str in list_of_filters]
    filter_func = lambda x: any(map(lambda pattern: pattern.match(x), patterns))
    return filter_func
