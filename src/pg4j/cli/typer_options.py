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
from pathlib import Path

import typer

from pg4j.cli.styles import LOGO_STYLE

# DEFAULT Constants
DEFAULT_DIRECTORY = Path.cwd()
# Build the typer options by setting default val, help str and abbreviations
build_typer_option = lambda default: lambda help_str, abbrev, envvar: typer.Option(
    default, *abbrev, help=help_str, envvar=envvar
)


def check_data_dir(directory: Path) -> Path:
    # Check directory exists and is empty
    if not directory.exists():
        directory.mkdir(exist_ok=True)

    for name in ("nodes", "edges"):
        if not (directory / name).exists():
            raise typer.BadParameter(f"Data-dir does not have {name} directory inside it!")
    return directory


def version_callback(value: bool):
    """
    Eagerly print the version LOGO

    Args:
        value (bool): [description]

    Raises:
        typer.Exit: exits after showing version
    """
    if value:
        typer.echo(LOGO_STYLE)
        raise typer.Exit()


PG4J_DATA_DIR_OPTION = typer.Option(
    [],
    "--data-dir",
    help="List of directories created from `pg4j dump` commands.",
    callback=lambda inputs: list(map(check_data_dir, inputs)),
)

DSN_OPTION = build_typer_option(None)(
    "Only run files that match this regex filter", ["--conn", "-c"], "PG4J__POSTGRES_SCHEMA"
)
NEO4J_HOME = environ.get("NEO4J_HOME", "/usr/local/var/neo4j/data/")
NEO4J_HOME_OPTION = build_typer_option(NEO4J_HOME)("Path to neo4j", ["--neo4j-home"], "NEO4J_HOME")

INCLUDE_FILTER = build_typer_option([r'.*'])
XCLUDE_FILTER = build_typer_option([])

COL_INCLUDE_FILTERS_OPTION = XCLUDE_FILTER(
    "Only include columns that match these regex filters", ["--col-include", "-ci"], None
)
TAB_INCLUDE_FILTERS_OPTION = INCLUDE_FILTER(
    "Include tables whose name matches these regex filters", ["--tab-include", "-ti"], None
)
COL_XCLUDE_FILTERS_OPTION = XCLUDE_FILTER(
    "Only include columns that match these regex filters", ["--col-exclude", "-cx"], None
)
TAB_XCLUDE_FILTERS_OPTION = XCLUDE_FILTER(
    "Include tables whose name matches these regex filters", ["--tab-exclude", "-tx"], None
)
FILE_INCLUDE_FILTERS_OPTION = INCLUDE_FILTER(
    "Only include files that match these regex filters", ["--include"], None
)
FILE_XCLUDE_FILTERS_OPTION = XCLUDE_FILTER(
    "Exclude tables whose name matches these regex filters", ["--exclude"], None
)


CONFIG_OPTION = typer.Option(None, "--config", "-c", help="Configuration file.")
SETTINGS_OPTION = typer.Option(None, "--config", help="Settings File.", envvar="PG4J_CONFIG")

VERSION_OPTION = typer.Option(
    None, "--version", "-v", help="Display version info.", callback=version_callback, is_eager=True
)
