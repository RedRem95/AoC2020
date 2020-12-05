import math
import random
from typing import Tuple, List

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
        log = [f"checking {len(self.get_input(task=task))} boarding passes"]
        seat_ids = [self._process_pass(boarding_pass=x)[-1] for x in self.get_input(task=task)]
        result = max(seat_ids)
        log.append(f"Minimum seat id found: {min(seat_ids)}")
        log.append(f"Maximum seat id found: {result}")
        return "\n".join(log), result

    def _run02(self, task: StarTask = StarTask.Task01) -> Tuple[str, object]:
        log = [f"checking {len(self.get_input(task=task))} boarding passes"]
        seat_ids = [self._process_pass(boarding_pass=x)[-1] for x in self.get_input(task=task)]
        empty_ids = [x for x in range(min(seat_ids), max(seat_ids), 1) if x not in seat_ids]
        log.append(f"Found {len(empty_ids)} empty seat{'s' if len(empty_ids) != 1 else ''}")
        if len(empty_ids) <= 0:
            log.append("Check first and last row")
            result = None
        else:
            result = random.choice(empty_ids)
            log.append(f"Found seats: [{', '.join(str(x) for x in empty_ids)}]")
            log.append(f"Selecting one by random. Your seat is {result}")
        return "\n".join(log), result

    @staticmethod
    def _process_pass(boarding_pass: str) -> Tuple[int, int, int]:

        def _separate(action_list: List[str], down_action: str, up_action: str) -> int:
            _not_defined_actions = [x for x in action_list if not (x == down_action or x == up_action)]
            if len(_not_defined_actions) > 0:
                raise ValueError(
                    f"Actions {_not_defined_actions} were not defined. Defined actions: {down_action}, {up_action}")
            _min = int(0)
            _max = int(math.pow(2, len(action_list)) - 1)
            for _action in action_list:
                if _action == down_action:
                    _max = int(_max - (_max - _min + 1) / 2)
                if _action == up_action:
                    _min = int(_min + (_max - _min + 1) / 2)
            if _min != _max:
                raise ValueError(f"Values generated from list {action_list} do not align. {_min} != {_max}")
            return _min

        _action_space_row = ("f", "b")
        _action_space_col = ("l", "r")

        row = _separate([x.lower() for x in boarding_pass if x.lower() in _action_space_row], *_action_space_row)
        col = _separate([x.lower() for x in boarding_pass if x.lower() in _action_space_col], *_action_space_col)

        return row, col, int(row * 8 + col)

    def get__file__(self) -> str:
        return __file__
