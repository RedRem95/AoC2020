from typing import Any
try:
    from packaging.version import parse
except ImportError:
    def parse(version: str) -> Any:
        return version

__VERSION = "0.15.0-Day15"


def get_version() -> Any:
    return parse(__VERSION)
