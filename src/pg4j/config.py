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

"""For parsing in config YAML."""
from pathlib import Path
from typing import Dict, List

import yaml

# from pydantic.dataclasses import dataclass
from pydantic import BaseModel, Field


class BaseModel(BaseModel):  # type: ignore
    class Config:
        """Pydantic Config."""

        extra = "forbid"


class DataDirectory(BaseModel):
    labels: List[str] = Field(default_factory=list)


class ColumnMapping(BaseModel):
    default: Dict[str, str] = Field(default_factory=lambda: {})
    table_maps: Dict[str, Dict[str, str]] = Field(default_factory=lambda: {})

    def get(self, table_name: str) -> Dict[str, str]:
        output = self.default.copy()
        output.update({k: v for k, v in self.table_maps.get(table_name, {}).items()})
        return output


class Pg4jConfig(BaseModel):
    """Pg4j Configuration File with Pydantic Validation."""

    data_dirs: Dict[Path, DataDirectory] = Field(default_factory=dict)
    column_mapping: ColumnMapping = Field(default_factory=ColumnMapping)

    @classmethod
    def from_yaml(cls, yaml_path: Path) -> "Pg4jConfig":
        config = {}
        if yaml_path:
            with open(yaml_path) as stream:
                try:
                    config = yaml.load(stream, Loader=yaml.SafeLoader)
                except yaml.YAMLError as exc:
                    print(exc)

        return cls.parse_obj(config)

    # @validator("data_dirs")
    # def directories_exist(cls, data_dirs: Dict[Path, DataDirectory]):
    #     for directory in data_dirs.keys():
    #         assert directory.exists(), 'Directory must exist'
