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

"""Welcome to pg4j"""

from pg4j.version import git_version, version

__author__ = "Modelyst LLC"
__email__ = "info@modelyst.io"
__maintainer__ = "Michael Statt"
__maintainer_email__ = "michael.statt@modelyst.io"
__version__ = version
__gitversion__ = git_version

LOGO = r"""
                 __ __  _
    ____  ____ _/ // / (_)
   / __ \/ __ `/ // /_/ /
  / /_/ / /_/ /__  __/ /
 / .___/\__, /  /_/_/ /
/_/    /____/    /___/
"""

PRINT_LOGO = f"""
--------------------------{LOGO}--------------------------
VERSION: {version}
GITVERSION: {git_version}
--------------------------
"""
