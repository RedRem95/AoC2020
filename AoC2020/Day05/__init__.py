import math
import random
from typing import Tuple

from AoC.Day import Day, StarTask


class Day05(Day):

    def __init__(self):
        super().__init__()

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        ret = []
        for line in [x for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]:
            ret.append(line)
        return ret

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(task=StarTask.Task01)
        if task == StarTask.Task02:
            return self._run02(task=StarTask.Task01)
        return "", None

    def _run01(self, task: StarTask = StarTask.Task01) -> Tuple[str, object]:
        log = [f"checking {len(self.get_input(task=task))} boarding passes for maximum id"]
        seat_ids = [self._process_pass(boarding_pass=x)[-1] for x in self.get_input(task=task)]
        result = max(seat_ids)
        log.append(f"Minimum id found as {min(seat_ids)}")
        log.append(f"Maximum id found as {result}")
        return "\n".join(log), result

    def _run02(self, task: StarTask = StarTask.Task01) -> Tuple[str, object]:
        log = [f"checking {len(self.get_input(task=task))} boarding passes for maximum id"]
        seat_ids = [self._process_pass(boarding_pass=x)[-1] for x in self.get_input(task=task)]
        empty_ids = [x for x in range(min(seat_ids), max(seat_ids), 1) if x not in seat_ids]
        log.append(f"Found {len(empty_ids)} empty seats")
        if len(empty_ids) <= 0:
            log.append("You cant fly here")
            result = None
        else:
            result = random.choice(empty_ids)
            log.append(f"Found seats: [{', '.join(str(x) for x in empty_ids)}]")
            log.append(f"Selected one by random. Your seat is {result}")
        return "\n".join(log), result

    def _process_pass(self, boarding_pass: str) -> Tuple[int, int, int]:
        _f_b = [x.lower() for x in boarding_pass if x.lower() in ["f", "b"]]
        _l_r = [x.lower() for x in boarding_pass if x.lower() in ["l", "r"]]

        _row_min = 0
        _row_max = int(math.pow(2, len(_f_b)) - 1)

        _col_min = 0
        _col_max = int(math.pow(2, len(_l_r)) - 1)

        for _e in _f_b:
            if _e == "f":
                _row_max = _row_max - (_row_max - _row_min + 1) / 2
            if _e == "b":
                _row_min = _row_min + (_row_max - _row_min + 1) / 2

        for _e in _l_r:
            if _e == "l":
                _col_max = _col_max - (_col_max - _col_min + 1) / 2
            if _e == "r":
                _col_min = _col_min + (_col_max - _col_min + 1) / 2

        if _row_min != _row_max or _col_min != _col_max:
            raise ValueError(f"Values not aligning {_row_min} != {_row_max}; {_col_min} != {_col_max}")

        return int(_row_min), int(_col_min), int(_row_min * 8 + _col_min)

    def get__file__(self) -> str:
        return __file__
