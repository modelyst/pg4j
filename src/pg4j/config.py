"""For parsing in config YAML."""
from pathlib import Path
import yaml


def read_config(config_path: Path) -> dict:
    config = None
    with open(config_path, "r") as stream:
        try:
            config = yaml.load(stream, Loader=yaml.SafeLoader)
        except yaml.YAMLError as exc:
            print(exc)

    return config
