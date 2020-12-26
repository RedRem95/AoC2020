import collections
from typing import Tuple, List, Dict, Optional

from AoC.Day import Day, StarTask


class Day23(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        cups = [int(y) for y in [x.strip() for x in str(raw_input, "utf-8").strip().split("\n")][0]]
        _ = sorted(cups)
        if any(_[i] + 1 != _[i + 1] for i in range(len(_) - 1)):
            raise Exception("You have atleast one jump in your cup labeling")
        return cups

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task is None:
            return "", None
        log, cups = self._run(cups=self.get_input(task=task), **self.get_day_config()[task.name])
        index_1 = cups.index(1)
        r: Optional[List[int]] = None
        if task == StarTask.Task01:
            r = [cups[(index_1 + i) % len(cups)] for i in range(1, len(cups), 1)]
            log.append(f"Cups after '1' are labelled {' '.join(str(x) for x in r)}")
        elif task == StarTask.Task02:
            wanted_cup_count = 2
            r = [cups[(index_1 + i) % len(cups)] for i in range(1, wanted_cup_count + 1, 1)]
            log.append(f"The {wanted_cup_count} cups after '1' are {' '.join(str(x) for x in r)}")
            _r = r[0]
            for _ in r[1:]:
                _r *= _
            r = [_r]
        return "\n".join(str(x) for x in log), None if r is None else "".join(str(x) for x in r)

    @staticmethod
    def _run(cups: List[int], rounds: int, target_amount: int, pick_up_count: int = 3) -> Tuple[List[str], List[int]]:
        log = [
            f"Playing against crab with {target_amount if target_amount > 0 else len(cups)} cups",
            f"First {len(cups)} cups are labeled {' '.join(str(x) for x in cups)}",
            "Rest of cups are filled automatically",
            f"Going to play {rounds} rounds",
            f"Picking up {pick_up_count} cups per turn"
        ]
        cups = cups + [i + 1 for i in range(max(cups), target_amount, 1)]
        min_cup, max_cup = min(cups), max(cups)
        picked_up: Dict[int, List[int]] = {}
        cups_queue = collections.deque(iterable=cups, maxlen=len(cups))

        def get_next() -> int:
            n = cups_queue.popleft()
            if n in picked_up:
                for v in reversed(picked_up[n]):
                    cups_queue.appendleft(v)
                del picked_up[n]
            return n

        i = 0
        while i < rounds:

            current = get_next()
            pick_up = [get_next() for _ in range(pick_up_count)]

            destination = current - 1
            while destination < min_cup or destination in pick_up:
                destination -= 1
                if destination < min_cup:
                    destination = max_cup

            picked_up[destination] = pick_up
            cups_queue.append(current)

            i += 1

        ret = []
        while len(cups_queue) > 0:
            ret.append(get_next())
        return log, ret
