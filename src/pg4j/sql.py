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

import sqlalchemy.dialects.postgresql as pg
from psycopg2.extensions import parse_dsn
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine, url
from sqlalchemy.sql import sqltypes


def get_conn(dsn: str, password: str = None):
    parsed_dsn = parse_dsn(dsn)
    new_url = url.URL(
        "postgresql+psycopg2",
        username=parsed_dsn["user"],
        host=parsed_dsn["host"],
        port=parsed_dsn.get("port", 5432),
        database=parsed_dsn["dbname"],
        password=password,
    )

    engine = create_engine(new_url)
    engine.connect()
    return engine


def read_schema(engine: Engine, schema: str):
    metadata = MetaData()
    metadata.reflect(bind=engine, schema=schema)
    return metadata


def dump_query(query: str, engine: Engine, path: Path):
    # set up our database connection.
    conn = engine.raw_connection()
    with conn.cursor() as cursor:

        # Use the COPY function on the SQL we created above.
        SQL_for_file_output = f"COPY ({query}) TO STDOUT WITH CSV HEADER"
        # Set up a variable to store our file path and name.
        with open(path, "w") as f_output:
            cursor.copy_expert(SQL_for_file_output, f_output)


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
