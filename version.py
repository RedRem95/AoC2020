from typing import Any
try:
    from packaging.version import parse
except ImportError:
    def parse(version: str) -> Any:
        return version

      
__VERSION = "0.24.0-Day24"


def get_version() -> Any:
    return parse(__VERSION)
