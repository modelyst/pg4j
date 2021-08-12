import re
from pathlib import Path
from typing import Callable, List

from sqlalchemy import ForeignKey as SAForeignKey
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.sql import sqltypes
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.engine import Engine

from .classes import ForeignKey

FILTER_FUNC_TYPE = Callable[[str], bool]


def get_conn(dsn: str):
    engine = create_engine(dsn)
    engine.connect()
    return engine


def snake_to_camel(string: str, first_capital: bool = False):
    first, *after = string.split("_")
    output = first.capitalize() if first_capital else first
    return output + "".join(map(lambda x: x.capitalize(), after))


def read_schema(engine: Engine, schema: str):
    metadata = MetaData()
    metadata.reflect(bind=engine, schema=schema)
    return metadata


def parse_table(
    table: Table,
    exclude_filter_func: FILTER_FUNC_TYPE,
    include_filter_func: FILTER_FUNC_TYPE,
) -> dict:
    primary_keys = [key.name for key in table.primary_key]
    if len(primary_keys) > 1:
        raise NotImplementedError("Haven't dealt with composite keys yet")
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


def dump_query(query: str, engine: Engine, path: Path):
    # set up our database connection.
    conn = engine.raw_connection()
    with conn.cursor() as cursor:

        # Use the COPY function on the SQL we created above.
        SQL_for_file_output = f"COPY ({query}) TO STDOUT WITH CSV HEADER"
        # Set up a variable to store our file path and name.
        with open(path, "w") as f_output:
            cursor.copy_expert(SQL_for_file_output, f_output)


def filters_to_filter_func(list_of_filters: List[str]) -> FILTER_FUNC_TYPE:
    # Compile filter func
    filter_func = lambda x: any(
        map(lambda pattern: re.findall(pattern, x), list_of_filters)
    )
    return filter_func


# Map Postgres types to neo4j type strings
# !TODO! Add all possible postgres types
PG_TO_NEO4J_TYPE_MAP = {
    sqltypes.INTEGER: "int",
    sqltypes.BIGINT: "long",
    sqltypes.NUMERIC: "float",
    sqltypes.DECIMAL: "float",
    sqltypes.BOOLEAN: "boolean",
    sqltypes.BINARY: "byte",
    sqltypes.VARCHAR: "string",
    sqltypes.TEXT: "string",
    sqltypes.DATE: "date",
    sqltypes.DATETIME: "datetime",
    sqltypes.DateTime: "datetime",
    sqltypes.TIMESTAMP: "string",
    pg.base.TIMESTAMP: "string",
    pg.base.BIGINT: "long",
    pg.json.JSON: "string",
    pg.json.JSONB: "string",
}

ALL_SQL_TYPES = [
    sqltypes.ARRAY,
    sqltypes.BIGINT,
    sqltypes.BigInteger,
    sqltypes.BINARY,
    sqltypes.BLOB,
    sqltypes.BOOLEAN,
    sqltypes.Boolean,
    sqltypes.CHAR,
    sqltypes.CLOB,
    sqltypes.Concatenable,
    sqltypes.DATE,
    sqltypes.Date,
    sqltypes.DATETIME,
    sqltypes.DateTime,
    sqltypes.DECIMAL,
    sqltypes.Enum,
    sqltypes.FLOAT,
    sqltypes.Float,
    sqltypes.Indexable,
    sqltypes.INT,
    sqltypes.INTEGER,
    sqltypes.Integer,
    sqltypes.Interval,
    sqltypes.JSON,
    sqltypes.LargeBinary,
    sqltypes.MatchType,
    sqltypes.NCHAR,
    sqltypes.NULLTYPE,
    sqltypes.NullType,
    sqltypes.NUMERIC,
    sqltypes.Numeric,
    sqltypes.NVARCHAR,
    sqltypes.PickleType,
    sqltypes.REAL,
    sqltypes.SchemaType,
    sqltypes.SMALLINT,
    sqltypes.SmallInteger,
    sqltypes.String,
    sqltypes.STRINGTYPE,
    sqltypes.TEXT,
    sqltypes.Text,
    sqltypes.TIME,
    sqltypes.Time,
    sqltypes.TIMESTAMP,
    sqltypes.Unicode,
    sqltypes.UnicodeText,
    sqltypes.VARBINARY,
    sqltypes.VARCHAR,
]
