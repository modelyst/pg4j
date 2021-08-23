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

import dataclasses
from collections.abc import Collection
from json import dumps
from typing import Dict, List

from sqlalchemy import Column as SAColumn
from sqlalchemy import ForeignKey as SAForeignKey
from sqlalchemy import Table as SATable
from sqlalchemy import Text, cast, select
from sqlalchemy.sql.expression import literal_column
from sqlalchemy.sql.schema import MetaData

from pg4j.sql import PG_TO_NEO4J_TYPE_MAP
from pg4j.utils import camel_to_snake, snake_to_camel


def dataclass_dict(thing):
    fields = dataclasses.fields(thing)
    if isinstance(thing, type):
        raise TypeError("got dataclass type, expected instance")

    exclude = getattr(thing, "_hash_exclude_", ())

    rv = {}
    for field in fields:
        if field.name in exclude:
            continue
        value = getattr(thing, field.name)
        if value is None or not value and isinstance(value, Collection):
            continue
        rv[field.name] = value

    return rv


def json_default(thing):
    """Custom"""
    try:
        return dataclass_dict(thing)
    except TypeError:
        pass
    print(thing)
    raise TypeError(f"object of type {type(thing).__name__} not serializable")


def json_dumps(thing):
    return dumps(
        thing,
        default=json_default,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
        separators=(",", ":"),
    )


class Base:
    def toJSON(self):
        return json_dumps(dataclasses.asdict(self))


@dataclasses.dataclass
class Column(Base):
    name: str
    dtype: str
    index: bool
    sa_col: SAColumn

    @classmethod
    def from_sqlalchemy(cls, col: SAColumn) -> "Column":
        return cls(name=col.name, dtype=col.type.__visit_name__, index=col.index, sa_col=col)


@dataclasses.dataclass
class PrimaryKey(Base):
    name: str
    dtype: str
    sa_col: SAColumn

    @classmethod
    def from_sqlalchemy(cls, col: SAColumn) -> "PrimaryKey":
        return cls(name=col.name, dtype=col.type.__visit_name__, sa_col=col)


@dataclasses.dataclass
class ForeignKey(Base):
    source_table: str
    source_column: str
    source_schema: str
    target_table: str
    target_column: str
    target_schema: str
    sa_foreign_key: SAForeignKey

    @classmethod
    def from_sqlalchemy(cls, sa_foreign_key: SAForeignKey) -> "ForeignKey":
        target_column = sa_foreign_key.column
        target_table = target_column.table
        source_column = sa_foreign_key.parent
        source_table = source_column.table
        foreign_key = ForeignKey(
            source_table.name,
            source_column.name,
            source_table.schema,
            target_table.name,
            target_column.name,
            target_table.schema,
            sa_foreign_key=sa_foreign_key,
        )
        return foreign_key

    def toSQL(self):
        target_column = self.sa_foreign_key.column
        target_table = target_column.table
        source_column = self.sa_foreign_key.parent
        source_table = source_column.table
        return select(
            [
                self.sa_foreign_key.parent.table.columns.id.label(
                    f":START_ID({snake_to_camel(source_table.name,True)})"
                ),
                self.sa_foreign_key.parent.label(f":END_ID({snake_to_camel(target_table.name,True)})"),
                literal_column("'" + camel_to_snake(target_table.name).upper() + "'").label(":TYPE"),
            ]
        ).filter(self.sa_foreign_key.parent != None)


@dataclasses.dataclass
class Table(Base):
    name: str
    schema: str
    primary_key: PrimaryKey
    columns: List[Column]
    foreign_keys: List[ForeignKey]
    sa_table: SATable

    @classmethod
    def from_sqlalchemy(cls, table: SATable) -> "Table":
        primary_keys = [key.name for key in table.primary_key]
        if len(primary_keys) > 1:
            raise NotImplementedError("Haven't dealt with composite keys yet")
        sa_primary_key = list(table.primary_key)[0]
        primary_key = PrimaryKey.from_sqlalchemy(sa_primary_key)
        columns = [
            Column.from_sqlalchemy(col)
            for col in table.columns
            if not col.primary_key and not col.foreign_keys
        ]
        foreign_keys = [
            ForeignKey.from_sqlalchemy(list(col.foreign_keys)[0]) for col in table.columns if col.foreign_keys
        ]

        return cls(
            name=table.name,
            schema=table.schema,
            primary_key=primary_key,
            columns=columns,
            foreign_keys=foreign_keys,
            sa_table=table,
        )

    def is_mapping_table(self, metadata: MetaData) -> bool:
        if not len(self.foreign_keys) == 2:
            return False

        for table in metadata.tables.values():
            for fk in table.foreign_keys:
                if fk.references(self.sa_table):
                    return False
        return True

    def toSQL(
        self,
        metadata: MetaData,
        include_columns_func,
        exclude_columns_func,
        col_map: Dict[str, str] = None,
        ignore_mapping: bool = False,
    ) -> str:

        # alias for columns
        col_map = col_map or {}
        select_cols = []
        for col in self.columns:
            if include_columns_func(col.name) and not exclude_columns_func(col.name):
                type_string = PG_TO_NEO4J_TYPE_MAP.get(type(col.sa_col.type), "string")

                if type(col.sa_col.type) not in PG_TO_NEO4J_TYPE_MAP:
                    print(f"No type mapping for type: {type(col.sa_col.type)}")
                col_name = col_map.get(col.name, col.name)
                alias = f"{col_name}:{type_string}"
                if isinstance(col.sa_col.type, ()):
                    select_cols.append(cast(col.sa_col.label(alias), Text))
                else:
                    select_cols.append(col.sa_col.label(alias))
        mapped_name = col_map.get("_alias")

        if not ignore_mapping and self.is_mapping_table(metadata):
            start, end = self.foreign_keys
            # Convention for mapping table is STARTTABLE__END_TABLE
            # Swap start and end if the table name begins with the ends table_name
            # Else the arrow direction is essentially random as defined by SqlAlchemy's ordering of FKs
            if self.name.startswith(end.target_table):
                temp = start
                start = end
                end = temp
            edge_type = mapped_name or camel_to_snake(end.target_table).upper()
            return select(
                [
                    start.sa_foreign_key.parent.label(
                        f":START_ID({snake_to_camel(start.target_table, True)})"
                    ),
                    end.sa_foreign_key.parent.label(f":END_ID({snake_to_camel(end.target_table,True)})"),
                    literal_column("'" + edge_type + "'").label(":TYPE"),
                    *select_cols,
                ]
            )
        label = mapped_name or snake_to_camel(self.name, True)
        return select(
            [
                self.primary_key.sa_col.label(
                    f"{snake_to_camel(self.name)}:ID({snake_to_camel(self.name, True)})"
                ),
                literal_column("'" + label + "'").label(":LABEL"),
                *select_cols,
            ]
        )
