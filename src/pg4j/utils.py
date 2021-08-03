from dbgen import ConnectInfo
from pathlib import Path


def get_conn():
    conn = ConnectInfo.from_aws_secret(
        "stage/ace-rhoai/db/jcap", "us-west-2", "tri", "development", "localhost", 5433
    )
    return conn


def dump_query(query: str, conn, path: Path):
    # set up our database connection.
    db_cursor = conn.cursor()

    # Use the COPY function on the SQL we created above.
    SQL_for_file_output = f"COPY ({query}) TO STDOUT WITH CSV HEADER"

    # Set up a variable to store our file path and name.
    with open(path, "w") as f_output:
        db_cursor.copy_expert(SQL_for_file_output, f_output)
