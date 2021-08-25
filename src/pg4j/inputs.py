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
from typing import Dict, List, Optional

import yaml
from pydantic import BaseModel, Field

# common field types
dict_field = Field(default_factory=lambda: {})
list_field = Field(default_factory=lambda: [])

# Disable extra fields to catch mispelled fields


class BaseModel(BaseModel):  # type: ignore
    class Config:
        """Pydantic Config."""

        extra = "forbid"


class DataDirectory(BaseModel):
    """A local directory to be imported"""

    labels: List[str] = list_field


class DefaultTableMap(BaseModel):
    column_map: Dict[str, str] = dict_field
    ignore_mapping: Optional[bool] = False
    added_labels: List[str] = list_field
    exclude: List[str] = list_field
    include: List[str] = list_field


class TableMap(DefaultTableMap):
    name: str
    alias: str = ""
    ignore_mapping: Optional[bool] = None


class ColumnMapping(BaseModel):
    default: DefaultTableMap = Field(default_factory=DefaultTableMap)
    table_maps: List[TableMap] = list_field

    def get_table_map(self, table_name: str) -> TableMap:
        table_map_dict = {tab.name: tab for tab in self.table_maps}
        table_map = table_map_dict.get(table_name, TableMap(name=table_name, **self.default.dict()))
        # Append the labels, include, and exclude values from default to the table_map
        table_map.added_labels = list(set(table_map.added_labels + self.default.added_labels))
        table_map.include = list(set(table_map.include + self.default.include))
        table_map.exclude = list(set(table_map.exclude + self.default.exclude))
        table_map.column_map = {**self.default.column_map, **table_map.column_map}
        # Use default value if ignore_mapping is not set
        if table_map.ignore_mapping is None:
            table_map.ignore_mapping = self.default.ignore_mapping
        return table_map


class Pg4jInputFile(BaseModel):
    """Pg4j Input File with Pydantic Validation."""

    @classmethod
    def from_yaml(cls, yaml_path: Path):
        config = {}
        if yaml_path:
            with open(yaml_path) as stream:
                try:
                    config = yaml.load(stream, Loader=yaml.SafeLoader)
                except yaml.YAMLError as exc:
                    print(exc)
        if config is None:
            config = {}
        return cls.parse_obj(config)


class Pg4jMapping(Pg4jInputFile):
    """Input File for the pg4j dump function for mapping a postgres database to importable neo4j csvs."""

    column_mapping: ColumnMapping = Field(default_factory=ColumnMapping)
    table_include: List[str] = Field(default_factory=lambda: [r".*"])
    table_exclude: List[str] = list_field
    column_include: List[str] = Field(default_factory=lambda: [r".*"])
    column_exclude: List[str] = list_field


class Pg4jImport(Pg4jInputFile):
    """Input file for the pg4j import function indicating which local directories are to be imported."""

    data_dirs: Dict[Path, DataDirectory] = Field(default_factory=dict)
