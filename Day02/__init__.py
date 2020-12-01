from typing import Tuple

from Day import Day, StarTask


class Day02(Day):

    def __init__(self):
        super().__init__()

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        pass

    def run(self, task: StarTask) -> Tuple[str, object]:
        return "Not yet done", None

    def get__file__(self) -> str:
        return __file__
