from typing import Tuple, List

from AoC.Day import Day, StarTask


class Day11(Day):
    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        pass

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(data=self.get_input(task=StarTask.Task01))
        if task == StarTask.Task01:
            return self._run02(data=self.get_input(task=StarTask.Task01))
        return "", None

    def _run01(self, data: List):
        log = []
        for data_line in data:
            pass
        return "\n".join(str(x) for x in log), None

    def _run02(self, data: List):
        log = []
        for data_line in data:
            pass
        return "\n".join(str(x) for x in log), None

    def get__file__(self) -> str:
        return __file__
