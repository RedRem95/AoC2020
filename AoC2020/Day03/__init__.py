from typing import Tuple

import numpy as np

from AoC.Day import Day, StarTask


class Day03(Day):

    def __init__(self):
        super().__init__()
        self.__free = "."
        self.__tree = "#"
        self.__move = np.array((1, 3))

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        ret = []

        for line in [x for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]:
            ret.append(line)
        return ret

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task in (x for x in StarTask):
            return self.__run(task=task)
        return "", None

    def __run(self, task: StarTask):
        data = self.get_input(task=StarTask.Task01)
        log = []
        result = 1
        for move in [np.array([x["down"], x["left"]]) for x in self.get_day_config()[task.name]]:
            log.append(f"Checking slope pattern down {move[0]}, left {move[1]}")
            tmp = 0
            pos = np.array([0, 0])
            while pos[0] < len(data):
                if data[pos[0]][pos[1] % len(data[pos[0]])] == self.__tree:
                    tmp += 1
                pos += move
            result *= tmp
        return "\n".join(str(x) for x in log), result

    def get__file__(self) -> str:
        return __file__
