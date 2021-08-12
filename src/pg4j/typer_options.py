from os import environ
from pathlib import Path

import typer

# DEFAULT Constants
USER = environ.get("USER", "postgres")
DEFAULT_DSN = f"postgresql://{USER}:@localhost/ssrl"
DEFAULT_DIRECTORY = Path.cwd()
# Build the typer options by setting default val, help str and abbreviations
build_typer_option = lambda default: lambda help_str, abbrev: typer.Option(
    default, *abbrev, help=help_str
)


def check_data_dir(directory: Path) -> bool:
    # Check directory exists and is empty
    if not directory.exists():
        directory.mkdir(exist_ok=True)

    for name in ("nodes", "edges"):
        if not (directory / name).exists():
            raise typer.BadParameter(
                f"Data-dir does not have {name} directory inside it!"
            )
    return directory


DIRECTORY_THAT_IS_EMPTY_OPTION = typer.Option(
    DEFAULT_DIRECTORY, "--data-dir", callback=check_data_dir
)

DSN_OPTION = build_typer_option(DEFAULT_DSN)(
    "Only run files that match this regex filter", ["--conn", "-c"]
)
NEO4J_HOME = environ.get("NEO4J_HOME", "/usr/local/var/neo4j/data/")
NEO4J_HOME_OPTION = build_typer_option(NEO4J_HOME)("Path to neo4j", ["--neo4j-home"])

INCLUDE_FILTER = build_typer_option([r".*"])
XCLUDE_FILTER = build_typer_option([])

COL_INCLUDE_FILTERS_OPTION = INCLUDE_FILTER(
    "Only include columns that match these regex filters", ["--col-include", "-ci"]
)
TAB_INCLUDE_FILTERS_OPTION = INCLUDE_FILTER(
    "Include tables whose name matches these regex filters", ["--tab-include", "-ti"]
)
COL_XCLUDE_FILTERS_OPTION = XCLUDE_FILTER(
    "Only include columns that match these regex filters", ["--col-exclude", "-cx"]
)
TAB_XCLUDE_FILTERS_OPTION = XCLUDE_FILTER(
    "Include tables whose name matches these regex filters", ["--tab-exclude", "-tx"]
)
FILE_INCLUDE_FILTERS_OPTION = INCLUDE_FILTER(
    "Only include files that match these regex filters", ["--include"]
)
FILE_XCLUDE_FILTERS_OPTION = XCLUDE_FILTER(
    "Exclude tables whose name matches these regex filters", ["--exclude"]
)
