from typing import Tuple

import numpy as np

from Day import Day, StarTask


class Day01(Day):

    def get__file__(self) -> str:
        return __file__

    def __init__(self):
        super().__init__()

    def convert_input(self, raw_input: bytes, task: StarTask):
        return [int(x) for x in str(raw_input, "utf-8").split("\n")]

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self.__run(num_inputs=2)
        if task == StarTask.Task02:
            return self.__run(num_inputs=3)

    def __run(self, num_inputs: int, task: StarTask = StarTask.Task01) -> Tuple[str, object]:
        if num_inputs <= 1:
            return f"ERROR: {num_inputs} <= 1", None
        data: np.narray = np.array(self.get_input(task=task))
        target = int(self.get_day_config()["target"])
        tmp = data
        for i in range(num_inputs - 1):
            tmp = np.add.outer(data, tmp)
        try:
            pos = np.array(np.where(tmp == target))[:, 0]
            result = np.multiply.reduce(data[pos])
            return f"Use points at line {', '.join(str(x + 1) for x in pos)}: {' * '.join(str(x) for x in data[pos])} = {result}", result
        except IndexError:
            return f"ERROR: {target} propably was not findable", None
