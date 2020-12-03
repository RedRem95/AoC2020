from typing import Any
try:
    from packaging.version import parse
except ImportError:
    def parse(version: str):
        return version

__VERSION = "0.2.0-Day02"


def get_version() -> Any:
    return parse(__VERSION)
