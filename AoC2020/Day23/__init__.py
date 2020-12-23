from copy import deepcopy
from typing import Tuple, List, Dict, Any, Optional

import numpy as np

from AoC.Day import Day, StarTask


class Day23(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        cups = [int(y) for y in [x.strip() for x in str(raw_input, "utf-8").strip().split("\n")][0]]
        _ = sorted(cups)
        if any(_[i] + 1 != _[i + 1] for i in range(len(_) - 1)):
            raise Exception("You have atleast one jump in your cup labeling")
        return cups

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task02:
            return "", None
        log, cups = self._run_v2(data=self.get_input(task=task), **self.get_day_config()[task.name])
        index_1 = cups.index(1)
        r: Optional[List[int]] = None
        if task == StarTask.Task01:
            r = [cups[(index_1 + i) % len(cups)] for i in range(1, len(cups), 1)]
            log = []
        elif task == StarTask.Task02:
            r = [cups[(index_1 + 1) % len(cups)] * cups[(index_1 + 2) % len(cups)]]
            log = []
        return "\n".join(str(x) for x in log), None if r is None else "".join(str(x) for x in r)

    @staticmethod
    def _run(data: List[int], rounds: int, target_amount: int, log: bool = False) -> Tuple[List[str], List[int]]:
        log = [] if log else None
        cups = data + [i + 1 for i in range(max(data), target_amount, 1)]
        current_pos = 0
        done_moves: List[List[int]] = [deepcopy(cups)]
        for i in range(rounds):
            move = perform_next(cups=cups, current_pos=current_pos)
            if log:
                log.append(f"--move {i + 1}--")
                log.append(f"Cups: {' '.join(f'({i})' if i == move['current'] else str(i) for i in cups)}")
                log.append(f"Pick up: {' '.join(str(i) for i in move['pick_up'])}")
                log.append(f"Destination: {move['destination']}")
                log.append("")
            cups = move["next_cups"]
            if cups in done_moves:
                print("RECURSION!!!")
                exit(0)
            done_moves.append(deepcopy(cups))
            current_pos = move["current_pos"] + 1
            if rounds > 1000 and i % 1000 == 0:
                print(f"{(i + 1) / rounds * 100:6.2f} [{i + 1}/{rounds}]")
        if log:
            log.append(f"--final--")
            log.append(f"Cups: {' '.join(str(i) for i in cups)}")
        return log, cups

    @staticmethod
    def _run_v2(data: List[int], rounds: int, target_amount: int) -> Tuple[List[str], List[int]]:
        log = []
        cups = data + [i + 1 for i in range(max(data), target_amount, 1)]
        cups = numpy_variant(cups=cups, rounds=rounds)
        return log, list(cups)


def perform_next(cups: List[int], current_pos: int, pick_up_count: int = 3) -> Dict[str, Any]:
    pick_up = [cups[(current_pos + i) % len(cups)] for i in range(1, pick_up_count + 1, 1)]
    current = cups[current_pos % len(cups)]
    destination = current - 1
    while destination < min(cups) or destination in pick_up:
        destination -= 1
        if destination < min(cups):
            destination = max(cups)

    for i in pick_up:
        cups.remove(i)
    destination_index = cups.index(destination) + 1
    next_cups = cups[:destination_index] + pick_up + cups[destination_index:]
    # for i in reversed(pick_up):
    #    next_cups.insert(destination_index, i)
    return {
        "cups": cups,
        "pick_up": pick_up,
        "current": current,
        "destination": destination,
        "next_cups": next_cups,
        "current_pos": next_cups.index(current)
    }


def numpy_variant(cups: List[int], rounds: int, pick_up_count: int = 3) -> np.ndarray:
    _destination_search_old = 0
    _destination_search_new = 0
    _new_line = 0
    l_c = len(cups)
    matrix = np.zeros(shape=(2, l_c), dtype=np.int32)
    matrix[0, :] = np.array(cups, dtype=np.int32)
    cups = np.array(cups, dtype=np.int32)
    now, prev = 0, 1
    i = 1
    while i <= rounds:
        now, prev = i % 2, (i - 1) % 2
        # matrix[now, :] = 0

        if i > 1 and (matrix[prev, :] == cups).all():
            print(f"LOOP at {i}")
            exit()

        destination_candidates = matrix[prev, pick_up_count + 1:]
        destination = np.argmin(destination_candidates)
        if destination_candidates[destination] > matrix[prev, 0]:
            destination = np.argmax(destination_candidates)

        destination += 1

        matrix[now, :destination] = matrix[prev, pick_up_count + 1:pick_up_count + destination + 1]
        matrix[now, destination:destination + pick_up_count] = matrix[prev, 1:pick_up_count + 1]
        matrix[now, destination + pick_up_count:-1] = matrix[prev, pick_up_count + destination + 1:]
        matrix[now, -1] = matrix[prev, 0]

        if rounds > 1000 and i % 1000 == 0:
            print(f"{i / rounds * 100:6.2f} [{i}/{rounds}]")
        i += 1
    return matrix[now]
