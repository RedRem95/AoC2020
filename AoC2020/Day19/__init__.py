from typing import Tuple, List

from AoC.Day import Day, StarTask


class Day18(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        return [x.strip() for x in str(raw_input, "utf-8").strip().split("\n") if len(x) > 0]

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task is not None:
            return self._run(data=self.get_input(task=task))
        return "", None

    def _run(self, data: List[str]) -> Tuple[str, object]:
        log = []
        r = 0

        return "\n".join(str(x) for x in log), r
