import typer

from .dump import dump
from .mapper import mapper
from .importer import importer

app = typer.Typer()

# Add subcommands
app.command("map")(mapper)
app.command("dump")(dump)
app.command("import")(importer)

# Run App
app()
