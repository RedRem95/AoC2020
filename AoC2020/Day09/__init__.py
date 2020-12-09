import itertools
from typing import Tuple, List, Optional

from AoC.Day import Day, StarTask

NUMPY_MODE = False
if NUMPY_MODE:
    import numpy as np
    from numpy import sum, min, max


class Day09(Day):
    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        ret = []
        for line in [x for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]:
            ret.append(int(line))
        if NUMPY_MODE:
            return np.array(ret)
        return ret

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(task=StarTask.Task01)
        if task == StarTask.Task02:
            return self._run02(task=StarTask.Task01)
        return "", None

    def _run01(self, task):
        preamble_length = self.get_day_config()["preamble_length"]
        weakness_i, weakness = self._find_weakness(data=self.get_input(task=task), preamble_length=preamble_length)
        log = ""
        if weakness_i > 0 and weakness is not None:
            log = f"{weakness} in line {weakness_i + 1} does not consist of a sum of two of the previous " \
                  f"{preamble_length} lines"
        return log, weakness

    def _run02(self, task):
        data = self.get_input(task=task)
        preamble_length = self.get_day_config()["preamble_length"]
        weakness_i, weakness = self._find_weakness(data=data, preamble_length=preamble_length)
        log = [f"Weakness is {weakness} in line {weakness_i + 1}"]
        for j in range(weakness_i + 1):
            for k in range(j + 1, weakness_i + 1):
                if weakness == sum(data[j:k]):
                    mi = min(data[j:k])
                    ma = max(data[j:k])
                    log.append(f"Found crack in serious of lines {j + 1} to {k} of length {k - j}")
                    log.append(f"Crack is {mi} + {ma} => {mi + ma}")
                    return "\n".join(str(x) for x in log), mi + ma
        return "", None

    @staticmethod
    def _find_weakness(data: List[int], preamble_length: int) -> Tuple[int, Optional[int]]:
        for i in range(preamble_length, len(data)):
            if not any(x + y == data[i] and x != y for x, y in itertools.product(data[i - preamble_length:i],
                                                                                 data[i - preamble_length:i])):
                return i, data[i]
        return -1, None

    def get__file__(self) -> str:
        return __file__
