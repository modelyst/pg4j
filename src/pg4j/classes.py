from typing import List, ForwardRef
from json import dumps
import dataclasses
from collections.abc import Collection
from sqlalchemy import (
    Column as SAColumn,
    ForeignKey as SAForeignKey,
    Table as SATable,
    select,
)
from sqlalchemy.sql.expression import label, literal_column
from sqlalchemy.sql.schema import MetaData


ForeignKey = ForwardRef("ForiegnKey")


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
        return cls(
            name=col.name, dtype=col.type.__visit_name__, index=col.index, sa_col=col
        )


@dataclasses.dataclass
class PrimaryKey(Base):
    name: str
    dtype: str
    sa_col: SAColumn

    @classmethod
    def from_sqlalchemy(cls, col: SAColumn) -> "PrimaryKey":
        return cls(name=col.name, dtype=col.type.__visit_name__, sa_col=col)


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
            ForeignKey.from_sqlalchemy(list(col.foreign_keys)[0])
            for col in table.columns
            if col.foreign_keys
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
        col_map: dict = None,
    ) -> str:
        from .utils import snake_to_camel

        # alias for columns
        col_map = col_map or {}
        select_cols = [
            col.sa_col.label(col_map.get(col.name, col.name))
            for col in self.columns
            if include_columns_func(col.name) and not exclude_columns_func(col.name)
        ]
        if self.is_mapping_table(metadata):
            left, right = self.foreign_keys
            return select(
                [
                    left.sa_foreign_key.parent.label(
                        f":START_ID({snake_to_camel(left.target_table, True)})"
                    ),
                    right.sa_foreign_key.parent.label(
                        f":END_ID({snake_to_camel(right.target_table,True)})"
                    ),
                    literal_column(
                        "'" + snake_to_camel(right.target_table, True) + "'"
                    ).label(":TYPE"),
                    *select_cols,
                ]
            )
        return select(
            [
                self.primary_key.sa_col.label(
                    f"{snake_to_camel(self.name)}:ID({snake_to_camel(self.name, True)})"
                ),
                literal_column("'" + snake_to_camel(self.name, True) + "'").label(
                    ":LABEL"
                ),
                *select_cols,
            ]
        )


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
        from .utils import snake_to_camel

        return select(
            [
                self.sa_foreign_key.parent.table.columns.id.label(
                    f":START_ID({snake_to_camel(self.source_table,True)})"
                ),
                self.sa_foreign_key.parent.label(
                    f":END_ID({snake_to_camel(self.target_table,True)})"
                ),
                literal_column(
                    "'" + snake_to_camel(self.target_table, True) + "'"
                ).label(":TYPE"),
            ]
        )
