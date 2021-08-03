import typer
from typing import List
from time import sleep
from pathlib import Path
from os import getcwd, listdir
from utils import get_conn, dump_query
import re

# DEFAULT Constants
ROOT_DIR = Path(getcwd())
SQL_DIR = ROOT_DIR / "sql"
OUTPUT_DIR = ROOT_DIR / "output"


def main(
    sql_folder: Path = typer.Option(
        SQL_DIR, "--sql", help="Folder to find nodes/ and edges/ sql files"
    ),
    output_folder: Path = typer.Option(
        OUTPUT_DIR, "--output", help="Folder to output results"
    ),
    sql_filters: List[str] = typer.Option(
        [r".*"], "--filter", help="Only run files that match this regex filter"
    ),
):
    # Setup connection
    cxn = get_conn()
    # conn = get_conn()
    # cxn = conn.connect()
    patterns = [re.compile(sql_filter) for sql_filter in sql_filters]
    filter_func = lambda x: any(map(lambda pattern: pattern.match(x), patterns))
    try:
        # Iterate through nodes and edges
        for entity_type in ("nodes", "edges"):
            # Setup the directories to read from
            data_dir_curr = output_folder / entity_type
            sql_dir_curr = sql_folder / entity_type
            data_dir_curr.mkdir(parents=True, exist_ok=True)
            sql_paths = listdir(sql_dir_curr)
            # Iterate through paths and dump sql query to a csv
            basenames = list(
                filter(filter_func, map(lambda x: x.replace(".sql", ""), sql_paths))
            )
            typer.echo(basenames)
            with typer.progressbar(
                basenames,
                label=f"Getting {entity_type}",
                item_show_func=lambda x: f"{x}",
            ) as basenames_prog:
                for basename in basenames_prog:
                    sql_command = (
                        (sql_dir_curr / (basename + ".sql")).read_text().strip(";")
                    )
                    dump_query(
                        sql_command,
                        cxn,
                        data_dir_curr / f"{basename}.csv",
                    )
                    sleep(0.2)
    finally:
        cxn.close()


if __name__ == "__main__":
    typer.run(main)
