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

from os import environ
from textwrap import dedent

import pytest
import utils
from hypothesis import given
from hypothesis import strategies as st
from pydantic import PostgresDsn, ValidationError

from pg4j.inputs import Pg4jImport, Pg4jMapping, TableMap
from pg4j.settings import Neo4jDsn, Pg4jSettings
from pg4j.sql import get_conn


@pytest.fixture(scope="function", autouse=True)
def tests_setup_and_teardown():
    """Clear environ before every function to remove set variables."""
    # Will be executed before the first test
    old_environ = dict(environ)

    yield
    # Will be executed after the last test
    environ.clear()
    environ.update(old_environ)


def test_mapping_file_load():
    for mapping_path in utils.GOOD_MAPPINGS:
        Pg4jMapping.from_yaml(mapping_path)


def test_setting_file_load():
    for settings_path in utils.GOOD_SETTINGS:
        Pg4jSettings(_env_file=settings_path)


def test_import_file_load():
    for import_path in utils.GOOD_IMPORTS:
        Pg4jImport.from_yaml(import_path)


def test_get_map():
    config = Pg4jMapping.from_yaml(utils.MAPPING_DIR / "simple_map.yaml")
    mapping = config.column_mapping
    none_map = mapping.get_table_map("non_existent_table")
    assert none_map == TableMap(name="non_existent_table", **mapping.default.dict())
    one_map = mapping.get_table_map("table_1")
    assert one_map.column_map["col1"] == "table_1_col1"
    assert one_map.column_map["col2"] == mapping.default.column_map["col2"]


def test_simple_settings_default():
    settings = Pg4jSettings()
    assert settings
    assert isinstance(settings, Pg4jSettings)
    assert isinstance(settings.postgres_dsn, PostgresDsn)
    assert settings.postgres_dsn.host == 'localhost'
    assert settings.postgres_dsn.user == 'postgres'
    assert settings.postgres_dsn.port == '5432'
    assert settings.postgres_dsn.password is None
    assert settings.neo4j_dsn.host == "localhost"
    assert settings.neo4j_dsn.user == "neo4j"
    assert settings.neo4j_dsn.password is None
    assert settings.neo4j_dsn.scheme == "neo4j"
    assert settings.neo4j_dsn.port == "7687"


def test_simple_settings_inputs():
    settings = Pg4jSettings(postgres_dsn="postgresql://test:test@test.com:8888/test")
    assert settings.postgres_dsn.host == 'test.com'
    assert settings.postgres_dsn.user == 'test'
    assert settings.postgres_dsn.port == '8888'
    assert settings.postgres_dsn.password == 'test'
    assert settings.postgres_dsn.path == '/test'

    with pytest.raises(ValidationError):
        Pg4jSettings(postgres_dsn="http://google.com")

    settings = Pg4jSettings(neo4j_dsn="neo4j://test:test@localhost/test")


bad_dsns = ["google.com", "postgresql://test:test@test.com:8888/test", "neo4j://test:test@/test", ""]


@pytest.mark.parametrize("dsn", bad_dsns)
def test_settings_bad_neo4j_dsn(dsn: str):
    with pytest.raises(ValidationError):
        Pg4jSettings(neo4j_dsn=dsn)


@given(st.builds(Pg4jSettings))
def test_hypothesis_settings(settings):
    assert isinstance(settings, Pg4jSettings)
    assert isinstance(settings.postgres_dsn, PostgresDsn)
    assert isinstance(settings.neo4j_dsn, Neo4jDsn)
    get_conn(settings.postgres_dsn, connect=False)


def test_settings_basic_env_vars():
    """Test that environmental variables can be used to set config variables."""
    environ["PG4J__POSTGRES_DSN"] = "postgresql://test_env:@localhost/test"
    environ["PG4J__postgres_password"] = "postgres_password"
    environ["PG4J__NEO4J_DSN"] = "bolt://test:@localhost/test"
    environ["pg4j__neo4j_password"] = "neo4j_password"

    settings = Pg4jSettings()
    assert settings.postgres_dsn.user == "test_env"
    assert settings.postgres_password.get_secret_value() == "postgres_password"
    assert settings.neo4j_dsn.user == "test"
    assert settings.neo4j_password.get_secret_value() == "neo4j_password"


def test_env_file(tmpdir):
    """Test that dotenv files can be used to set config variables."""
    temp_env = tmpdir.mkdir("sub").join("env_file")
    env_file = """
    PG4J__POSTGRES_DSN = postgresql://test:@localhost/test
    PG4J__postgres_password = postgres_password
    PG4J__NEO4J_DSN = bolt://test:@localhost/test
    pg4j__neo4j_password = neo4j_password """
    temp_env.write(dedent(env_file))
    settings = Pg4jSettings(_env_file=temp_env)
    assert settings.postgres_dsn.user == "test"
    assert settings.postgres_password.get_secret_value() == "postgres_password"
    assert settings.neo4j_dsn.user == "test"
    assert settings.neo4j_password.get_secret_value() == "neo4j_password"
    environ["PG4J_CONFIG"] = str(temp_env)
    settings = Pg4jSettings(_env_file=environ.get("PG4J_CONFIG"))
    assert settings.postgres_dsn.user == "test"
    assert settings.postgres_password.get_secret_value() == "postgres_password"
    assert settings.neo4j_dsn.user == "test"
    assert settings.neo4j_password.get_secret_value() == "neo4j_password"

    environ["PG4J_CONFIG"] = ""
    settings = Pg4jSettings(_env_file=environ.get("PG4J_CONFIG"))
    assert settings.postgres_dsn.user == "postgres"
    assert settings.postgres_password.get_secret_value() == ""
    assert settings.neo4j_dsn.user == "neo4j"
    assert settings.neo4j_password.get_secret_value() == ""


def test_bad_env_file(tmpdir):
    """Test that dotenv files can be used to set config variables."""
    temp_env = tmpdir.mkdir("sub").join("env_file")
    env_file = """
    PG4J__POSTGRES_Dskldjhfgksjdhflkjsh lkjhsdfjhg lsjdfkjhg sdlfkjhg sjh====== = === =
    PG4J__POSTGRES_DSN = test://test:@localhost/test
    PG4J__POSTGRES_DSN = postgresql://test:@localhost/test
    PG4J__postgres_password = postgres_password
    PG4J__NEO4J_DSN = neo4j://test:@localhost/test
    pg4j__neo4j_password = neo4j_password """
    temp_env.write(dedent(env_file))
    settings = Pg4jSettings(_env_file=temp_env)
    assert settings.postgres_dsn.user == "test"
    assert settings.postgres_password.get_secret_value() == "postgres_password"
    assert settings.neo4j_dsn.user == "test"
    assert settings.neo4j_password.get_secret_value() == "neo4j_password"


def test_override_settings():
    override_settings = {
        "postgres_dsn": "postgresql://override:@localhost/test",
        "postgres_password": "override",
    }
    config_file = ".env"
    settings = Pg4jSettings(_env_file=config_file, **override_settings)
    assert settings.postgres_dsn.user == 'override'
    assert settings.postgres_password.get_secret_value() == 'override'
