"""For parsing in config."""
import typer
from .typer_options import DSN_OPTION
from .utils import get_conn


def test_conn(
    dsn: str = DSN_OPTION,
    db_password: str = typer.Option(
        None, prompt=True, confirmation_prompt=True, hide_input=True
    ),
):
    print(get_conn(dsn, password=db_password))
