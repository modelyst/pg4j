import typer

from .dump import dump
from .mapper import mapper
from .importer import importer
from .config import test_conn

app = typer.Typer()

# Add subcommands
app.command("map")(mapper)
app.command("dump")(dump)
app.command("import")(importer)
app.command("test")(test_conn)

# Run App
app()
