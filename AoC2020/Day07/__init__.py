from typing import Tuple

from AoC.Day import Day, StarTask


class Day07(Day):
    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        ret = []
        for line in [x for x in str(raw_input, "utf-8").split("\n")]:
            ret.append(line)
        return ret

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(task=StarTask.Task01)
        if task == StarTask.Task01:
            return self._run02(task=StarTask.Task02)
        return "", None

    def _run01(self, task: StarTask) -> Tuple[str, object]:
        log = []
        data = self.get_input(task=task)
        result = 0
        for data_line in data:
            result += len(data_line)
        return "\n".join(str(x) for x in log), result

    def _run02(self, task: StarTask) -> Tuple[str, object]:
        log = []
        data = self.get_input(task=task)
        result = 0
        for data_line in data:
            result += len(data_line)
        return "\n".join(str(x) for x in log), result

    def get__file__(self) -> str:
        return __file__
