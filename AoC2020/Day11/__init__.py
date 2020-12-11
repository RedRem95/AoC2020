import itertools
from enum import Enum
from typing import Tuple, List, Optional, Callable, Union

from AoC.Day import Day, StarTask
from AoC2020.Day11.GameOfSeats import Places, Stage, IH8PPL, ItsFreeRealEstate, FloorIsFloor, Rule, ViewingStage


class Day11(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        return [[Places.by_value(y) for y in x] for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run(raw_stage=self.get_input(task=StarTask.Task01),
                             rules=[FloorIsFloor(), ItsFreeRealEstate(), IH8PPL(4)],
                             stage_class=Stage)
        if task == StarTask.Task02:
            return self._run(raw_stage=self.get_input(task=StarTask.Task01),
                             rules=[FloorIsFloor(), ItsFreeRealEstate(), IH8PPL(5)],
                             stage_class=ViewingStage)
        return "", None

    @staticmethod
    def _run(stage_class, raw_stage: List[Union[Places, str]], rules: List[Rule]):
        stage = stage_class(data=raw_stage, rules=rules)
        max_iterations = 100_000
        i = stage.find_stable(max_iterations=max_iterations)
        if i is None:
            return f"Could not find a stable stage in {max_iterations} simulation steps", None
        log = [f"It took {i} iterations to reach a fixed and stable stage"] +\
              [f"There are now {stage.count(x)} {x.name}" for x in Places]
        return "\n".join(str(x) for x in log), stage.count(Places.OCCUPIED)

    def get__file__(self) -> str:
        return __file__
