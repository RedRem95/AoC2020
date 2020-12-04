from typing import Tuple

from AoC.Day import Day, StarTask


class Day05(Day):

    def __init__(self):
        return
        super().__init__()

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        pass

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(task=StarTask.Task01)
        if task == StarTask.Task02:
            return self._run02(task=StarTask.Task01)
        return "", None

    def _run01(self, task: StarTask = StarTask.Task01) -> Tuple[str, object]:
        log = []
        result = 0
        data = self.get_input(task=task)
        for data_line in data:
            result += 1
        return "\n".join(log), result

    def _run02(self, task: StarTask = StarTask.Task01) -> Tuple[str, object]:
        log = []
        result = 0
        data = self.get_input(task=task)
        for data_line in data:
            result += 1
        return "\n".join(log), result

    def get__file__(self) -> str:
        return __file__
