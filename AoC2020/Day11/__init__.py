import itertools
from enum import Enum
from typing import Tuple, List, Optional

from AoC.Day import Day, StarTask


class Day11(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        return [[Places.by_value(y) for y in x] for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(stage_1=self.get_input(task=StarTask.Task01))
        if task == StarTask.Task01:
            return self._run02(data=self.get_input(task=StarTask.Task01))
        return "", None

    def _run01(self, stage_1: List[List["Places"]]):
        print(self.stage_to_string(stage_1))
        print("-----------------------------------------------")
        stage_2 = self.next_stage(stage_1)
        while not self.compare_stages(stage_2, stage_1):
            print(self.stage_to_string(stage_2))
            print("-----------------------------------------------")
            stage_2, stage_1 = self.next_stage(stage_2), stage_2
        log = ["".join(str(y) for y in x) for x in stage_2]
        print(self.stage_to_string(stage_2))
        print("-----------------------------------------------")
        counting = sum(sum(1 if y == Places.OCCUPIED else 0 for y in x) for x in stage_2)
        return "\n".join(str(x) for x in log), counting

    def _run02(self, data: List):
        log = []
        for data_line in data:
            pass
        return "\n".join(str(x) for x in log), None

    @staticmethod
    def stage_to_string(stage: List[List["Places"]]):
        if stage is None:
            return ""
        return "\n".join("".join(str(y) for y in x) for x in stage)

    @staticmethod
    def next_stage(data: List[List["Places"]]) -> List[List["Places"]]:
        new_stage: List[List["Places"]] = [[]]

        for l, line in enumerate(data):
            for s, seat in enumerate(line):
                adjacent = _get_adjacent(x=s, y=l, min_y=0, min_x=0, max_x=len(line) - 1, max_y=len(data) - 1)
                if seat == Places.FLOOR:
                    new_stage[-1].append(Places.FLOOR)
                elif seat == Places.EMPTY:
                    if all(data[i][j] in (Places.EMPTY, Places.FLOOR) for i, j in adjacent):
                        new_stage[-1].append(Places.OCCUPIED)
                    else:
                        new_stage[-1].append(Places.EMPTY)
                elif seat == Places.OCCUPIED:
                    if sum(1 if data[i][j] == Places.OCCUPIED else 0 for i, j in adjacent) >= 4:
                        new_stage[-1].append(Places.EMPTY)
                    else:
                        new_stage[-1].append(Places.OCCUPIED)
            new_stage.append([])

        return [x for x in new_stage if len(x) > 0]

    @staticmethod
    def compare_stages(stage_1: List[List["Places"]], stage_2: List[List["Places"]]) -> bool:
        if stage_1 is None or stage_2 is None:
            return False
        if len(stage_1) != len(stage_2):
            return False

        for line_1, line_2 in zip(stage_1, stage_2):
            if len(line_1) != len(line_2):
                return False
            for element_1, element_2 in zip(line_1, line_2):
                if element_1 != element_2:
                    return False

        return True

    def get__file__(self) -> str:
        return __file__


def _get_adjacent(x: int, y: int, min_x: int, max_x: int, min_y: int, max_y: int) -> List[Tuple[int, int]]:
    ret: List[Tuple[int, int]] = []
    for i, j in itertools.product(range(-1, 2, 1), repeat=2):
        if i == 0 and j == 0:
            continue
        ret.append((x + i, y + j))
    return [t for t in ret if min_x <= t[0] <= max_x and min_y <= t[1] <= max_y]


class Places(Enum):
    FLOOR = ".",
    EMPTY = "L",
    OCCUPIED = "#"

    def __str__(self):
        return str(self.value[0] if hasattr(self.value, "__iter__") else self.value)

    @classmethod
    def by_value(cls, val: str) -> Optional["Places"]:
        for i in cls:
            if val == str(i):
                return i
        return None
