from typing import Tuple, List

from AoC.Day import Day, StarTask


class Day13(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        return [x for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]

    def get__file__(self) -> str:
        return __file__

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(data=self.get_input(task=StarTask.Task01))
        if task == StarTask.Task01:
            return self._run02(data=self.get_input(task=StarTask.Task01))
        return "", None

    def _run01(self, data: List) -> Tuple[str, object]:
        log = []
        result = 0
        for data_line in data:
            result += data_line.__len__()
        return "\n".join(str(x) for x in log), result

    def _run02(self, data: List) -> Tuple[str, object]:
        log = []
        result = 0
        for data_line in data:
            result += data_line.__len__()
        return "\n".join(str(x) for x in log), result
