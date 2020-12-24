from typing import Tuple, List

from AoC.Day import Day, StarTask
from AoC2020.Day17.GameOfStates import GameOfStates, ItsAlive, ItsDead, DefaultState


class Day17(Day):
    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        return [[y for y in x.strip()] for x in str(raw_input, "utf-8").strip().split("\n") if len(x) > 0]

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task is not None:
            return self._run(data=self.get_input(task=task), **self.get_day_config()[task.name])
        return "", None

    def _run(self, data: List[List[str]], steps: int = 6, dimensions: int = 3) -> Tuple[str, object]:
        log = []
        dimension = GameOfStates(initial_plane=data,
                                 rules=[ItsAlive(), ItsDead()],
                                 dimensions=dimensions,
                                 interesting_states=[DefaultState.ACTIVE])
        r = dimension.count(DefaultState.ACTIVE)
        log.append(f"Setup a {dimension.get_dimensionality()}-d pocket dimension that has {r} initial active cores")
        for i in range(steps):
            dimension.next()
        r = dimension.count(DefaultState.ACTIVE)
        log.append(f"After {steps} steps this {dimension.get_dimensionality()}-d pocket dimension has {r} active cores")
        return "\n".join(str(x) for x in log), dimension.count(DefaultState.ACTIVE)
