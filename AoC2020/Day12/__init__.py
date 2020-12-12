from typing import Tuple, List

from AoC.Day import Day, StarTask
from AoC2020.Day12.Ship import Ship


class Day12(Day):
    def get__file__(self) -> str:
        return __file__

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        return [x for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]

    def run(self, task: StarTask) -> Tuple[str, object]:
        return self._run(data=self.get_input(task=StarTask.Task01), task=task)

    def _run(self, data: List[str], task: StarTask) -> Tuple[str, object]:
        if task is None:
            return "", None
        ship = Ship(pos=(0, 0), waypoint=tuple(self.get_day_config()[task.name]), waypoint_mode=task == StarTask.Task02)
        log = [
            "Starting ship",
            f"  Starting Position: {ship.get_pos()}",
            f"  Original Waypoint: {ship.get_waypoint()}",
            f"      Waypoint Mode: {ship.in_waypoint_mode()}"
        ]
        counter = 0
        for data_line in data:
            orig_pos = ship.get_pos()
            if ship.parse(instruction=data_line):
                if len(data) <= 5:
                    log.append(f"{data_line:5s}: {str(orig_pos):7s} -> {str(ship.get_pos()):7s}")
                counter += 1
        log.append(f"The ship executed {counter / len(data) * 100:6.2f}% [{counter}/{len(data)}] instructions")
        log.append(f"     Final Position: {ship.get_pos()}")
        log.append(f"     Final Waypoint: {ship.get_waypoint()}")
        log.append(f"   Driven Manhattan: {ship.manhattan_from_start()}")
        return "\n".join(str(x) for x in log), ship.manhattan_from_start()
