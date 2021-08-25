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

import typer

from pg4j.cli.settings import show_settings
from pg4j.cli.typer_options import version_callback
from pg4j.dump import dump
from pg4j.importer import importer

app = typer.Typer()

# Add subcommands
app.command("dump", short_help="Dump a postgres DB to a data directory.")(dump)
app.command("import", short_help="Import pg4j data directories into neo4j.")(importer)
app.command("version", short_help="Display pg4j version info.")(lambda: version_callback(True))
app.command("settings", short_help="Display pg4j settings info.")(show_settings)
