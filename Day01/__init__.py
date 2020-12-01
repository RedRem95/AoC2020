from typing import Tuple

try:
    import numpy as np
except ImportError:
    print("It seams like numpy is not installed. You absolutely need numpy to run this")
    exit(1)

from Day import Day, StarTask


class Day01(Day):

    def get__file__(self) -> str:
        return __file__

    def __init__(self):
        super().__init__()

    def convert_input(self, raw_input: bytes, task: StarTask):
        return [int(x) for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self.__run(num_inputs=2)
        if task == StarTask.Task02:
            return self.__run(num_inputs=3)

    def __run(self, num_inputs: int, task: StarTask = StarTask.Task01) -> Tuple[str, object]:
        if num_inputs <= 1:
            return f"ERROR: {num_inputs} <= 1", None
        data = self.get_input(task=task)
        if data is None or len(data) <= 0:
            return f"ERROR: input not defined correctly", None
        data: np.narray = np.array(data)
        target = int(self.get_day_config()["target"])
        tmp = data
        for i in range(num_inputs - 1):
            tmp = np.add.outer(data, tmp)
        try:
            pos = np.array(np.where(tmp == target))[:, 0]
            result = np.multiply.reduce(data[pos])
            return f"Search for {num_inputs} points that give {target} in summary\n" \
                   f"Use points at line {', '.join(f'{x + 1}->{data[x]}' for x in pos)}\n" \
                   f"{' * '.join(str(x) for x in data[pos])} = {target}", result
        except IndexError:
            return f"ERROR: {target} propably was not findable", None
