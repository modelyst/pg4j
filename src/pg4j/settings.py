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
import os
from textwrap import dedent
from typing import Dict, Union

# from pydantic.dataclasses import dataclass
from pydantic import AnyUrl, BaseSettings, PostgresDsn, SecretStr


# Settings Value
class Neo4jDsn(AnyUrl):
    allowed_schemes = {'neo4j', 'bolt'}
    user_required = True
    path: str

    @classmethod
    def validate_parts(cls, parts: Dict[str, str]) -> Dict[str, str]:
        defaults = {
            'port': '7687',
            'path': '/neo4j',
        }
        for key, value in defaults.items():
            if not parts[key]:
                parts[key] = value
        return super().validate_parts(parts)


class MySQLDsn(AnyUrl):
    allowed_schemes = {'mysql'}
    user_required = True
    path: str

    @classmethod
    def validate_parts(cls, parts: Dict[str, str]) -> Dict[str, str]:
        defaults = {
            'port': '3306',
        }
        for key, value in defaults.items():
            if not parts[key]:
                parts[key] = value
        return super().validate_parts(parts)


# Force postgresql schemes for connection for sqlalchemy
class PostgresqlDsn(PostgresDsn):
    allowed_schemes = {"postgresql","postgresql+psycopg"}
    path: str


class Pg4jSettings(BaseSettings):
    """Settings for the pg4j, especially database connections."""

    postgres_dsn: Union[PostgresqlDsn, MySQLDsn] = "postgresql://postgres@localhost:5432/pg4j"  # type: ignore
    postgres_password: SecretStr = ""  # type: ignore
    postgres_schema: str = "public"
    neo4j_dsn: Neo4jDsn = "neo4j://neo4j@localhost:7687/neo4j"  # type: ignore
    neo4j_password: SecretStr = ""  # type: ignore

    class Config:
        """Pydantic configuration"""

        env_file = os.environ.get("PG4J_CONFIG", ".env")
        env_prefix = "PG4J__"
        extra = "forbid"

    def display(self, show_passwords: bool = False):
        params = [
            "pg4j__{} = {}".format(
                key, val.get_secret_value() if show_passwords and "password" in key else val
            )
            for key, val in self.dict().items()
        ]
        params_str = "\n".join(params)
        output = f"""# Pg4j Settings\n{params_str}"""
        return dedent(output)

    def __str__(self):
        return self.display()

    def __repr__(self):
        return self.display()
