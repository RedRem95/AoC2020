from typing import Tuple, List

from AoC.Day import Day, StarTask


class Day23(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        return [x.strip() for x in str(raw_input, "utf-8").strip().split("\n")]

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(data=self.get_input(task=task))
        if task == StarTask.Task02:
            return self._run02(data=self.get_input(task=task))
        return "", None

    def _run01(self, data: List[str]) -> Tuple[str, object]:
        log = []
        r = None
        return "\n".join(str(x) for x in log), r

    def _run02(self, data: List[str]) -> Tuple[str, object]:
        log = []
        r = None
        return "\n".join(str(x) for x in log), r