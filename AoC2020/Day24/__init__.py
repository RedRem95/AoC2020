from typing import Tuple, List

from AoC.Day import Day, StarTask
from AoC2020.Day24.Floor import Floor, Colors, COLOR_BLACK, COLOR_WHITE


class Day24(Day):
    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        return [x.strip() for x in str(raw_input, "utf-8").strip().split("\n") if len(x) > 0]

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task is not None:
            return self._run01(data=self.get_input(task=task), **self.get_day_config()[task.name])
        return "", None

    @staticmethod
    def _run01(data: List[str], rounds_play: int = 0) -> Tuple[str, object]:
        log = []
        floor = Floor(default_color=COLOR_WHITE, starting_tile=(0, 0))
        floor.parse(tile_identifications=data)
        for _ in range(rounds_play):
            floor.next()
        r = floor.count(target_state=COLOR_BLACK)
        return "\n".join(str(x) for x in log), r
