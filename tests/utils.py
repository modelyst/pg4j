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
from pathlib import Path
from typing import List

DATA_DIR = Path(__file__).parent / "data"

SETTINGS_DIR = Path(__file__).parent / "data" / "settings"
GOOD_SETTINGS = list(SETTINGS_DIR.glob("*.yaml"))
MALFORMED_SETTINGS = list((SETTINGS_DIR / "malformed").glob("*.yaml"))

MAPPING_DIR = Path(__file__).parent / "data" / "mapping_files"
GOOD_MAPPINGS = list(MAPPING_DIR.glob("*.yaml"))
MALFORMED_MAPPINGS = (MAPPING_DIR / "malformed").glob("*.yaml")

IMPORT_DIR = Path(__file__).parent / "data" / "import_files"
GOOD_IMPORTS = list(IMPORT_DIR.glob("*.yaml"))
MALFORMED_IMPORTS = list((IMPORT_DIR / "malformed").glob("*.yaml"))


def get_ids(path_list: List[Path]) -> List[str]:
    return [x.name for x in path_list]
