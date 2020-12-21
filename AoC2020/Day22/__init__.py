from typing import Tuple, List

from AoC.Day import Day, StarTask


class Day21(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        ret = []
        for line in [x.strip() for x in str(raw_input, "utf-8").strip().split("\n") if len(x) > 0]:
            line = line.split(":")
            ret.append((line[0], ":".join(line[1:])))
        return ret

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(data=self.get_input(task=task))
        if task == StarTask.Task02:
            return self._run02(data=self.get_input(task=task))
        return "", None

    @staticmethod
    def _run01(data: List[str]) -> Tuple[str, object]:
        log = []
        return "\n".join(str(x) for x in log), None

    @staticmethod
    def _run02(data: List[str]) -> Tuple[str, object]:
        log = []
        return "\n".join(str(x) for x in log), None
