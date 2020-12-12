from typing import Any
try:
    from packaging.version import parse
except ImportError:
    def parse(version: str) -> Any:
        return version

__VERSION = "0.11.0-Day11"


def get_version() -> Any:
    return parse(__VERSION)
