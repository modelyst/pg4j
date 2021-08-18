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

import logging
from os.path import dirname, join

logger = logging.getLogger(__name__)
PG4J_ROOT = join(dirname(__file__), "../../")


def get_git_version(version_: str):
    """
    Writes the current git version to git_version if this is a git repo

    Args:
        version_ (str): the semantic version to prepend to file

    Returns:
        str: the full version with git
    """
    try:
        import git  # type: ignore

        try:
            repo = git.Repo(join(*[PG4J_ROOT, ".git"]))
        except git.NoSuchPathError:
            logger.warning(".git directory not found: Cannot compute the git version")
            return ""
        except git.InvalidGitRepositoryError:
            logger.warning("Invalid .git directory not found: Cannot compute the git version")
            return ""
    except ImportError as exc:
        logger.warning("gitpython not found: Cannot compute the git version.")
        raise exc

    if repo:
        sha = repo.head.commit.hexsha
        if repo.is_dirty():
            return f".dev0+{sha}.dirty"
        # commit is clean
        return f".release:{version_}+{sha}"
    return "no_git_version"


if __name__ == '__main__':
    from pg4j.version import version

    git_version = get_git_version(version)
    version_pth = join(PG4J_ROOT, "src/pg4j/git_version")
    with open(version_pth, "w") as f:
        f.write(git_version)
