from typing import Tuple, List

from AoC.Day import Day, StarTask


class Day12(Day):
    def get__file__(self) -> str:
        return __file__

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        ret = []
        for line in [x for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]:
            ret.append(int(line))
        return ret

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(data=self.get_input(task=StarTask.Task01))
        if task == StarTask.Task02:
            return self._run02(data=self.get_input(task=StarTask.Task01))
        return "", None

    def _run01(self, data: List[int]) -> Tuple[str, object]:
        log = []
        result = 0
        for data_line in data:
            result += 1
        return "\n".join(str(x) for x in log), result

    def _run02(self, data: List[int]):
        log = []
        result = 0
        for data_line in data:
            result += 1
        return "\n".join(str(x) for x in log), result
