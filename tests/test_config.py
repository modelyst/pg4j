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

import pytest
from pydantic import ValidationError
from utils import CONFIG_DIR, CONFIGS

from pg4j.config import DataDirectory, Pg4jConfig

BAD_CONFIGS = list((CONFIG_DIR / "bad_configs").glob("*.yaml"))
BAD_CONFIGS_IDS = list(map(lambda x: x.name, BAD_CONFIGS))


def test_basic_config():
    for config_pth in CONFIGS:
        config = Pg4jConfig.from_yaml(config_pth)
        assert config
        assert config.column_mapping
        assert filter(lambda x: isinstance(DataDirectory), config.data_dirs)


@pytest.mark.parametrize("config_path", BAD_CONFIGS, ids=BAD_CONFIGS_IDS)
def test_bad_config(config_path: Path):
    with pytest.raises(ValidationError):
        Pg4jConfig.from_yaml(config_path)


def test_get_map():
    config = Pg4jConfig.from_yaml(CONFIG_DIR / "simple_map.yaml")
    mapping = config.column_mapping
    none_map = mapping.get("non_existent_table")
    assert none_map == mapping.default
    one_map = mapping.get("table_1")
    assert one_map["col1"] == "table_1_col1"
    assert one_map["col2"] == mapping.default["col2"]
