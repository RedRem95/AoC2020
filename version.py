from typing import Any
try:
    from packaging.version import parse
except ImportError:
    def parse(version: str):
        return version

__VERSION = "0.1.0-Day01"


def get_version() -> Any:
    return parse(__VERSION)
