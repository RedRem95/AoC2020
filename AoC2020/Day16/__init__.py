from typing import Tuple, List, Dict

import numpy as np

from AoC.Day import Day, StarTask


class Day16(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        return self._parse_data(data=[x.strip() for x in str(raw_input, "utf-8").strip().split("\n")])

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(data=self.get_input(task=task))
        if task == StarTask.Task02:
            return self._run02(data=self.get_input(task=task))
        return "", None

    @staticmethod
    def _run01(data: Tuple[list["Class"], List[int], List[List[int]]]) -> Tuple[str, object]:
        other_tickets = np.array(data[2], dtype=int).flatten()
        log = f"There are {len(data[0])} classes to be checked\n" \
              f"There are {len(data[2])} other tickets you are scanning"
        return log, sum(0 if any(x.number_valid(y) for x in data[0]) else y for y in other_tickets)

    def _run02(self, data: Tuple[list["Class"], List[int], List[List[int]]]) -> Tuple[str, object]:
        log = [f"There are {len(data[0])} classes to be checked",
               f"There are {len(data[2])} other tickets you are scanning"]
        other_tickets = []
        classes = data[0]
        own_ticket = data[1]
        return_fields = self.get_day_config()["interesting_fields"]
        for ticket in data[2]:
            if len(ticket) == len(classes) and all(any(x.number_valid(y) for x in classes) for y in ticket):
                other_tickets.append(ticket)
        pos_valid_classes: Dict[int, List["Class"]] = {}
        for i in range(len(classes)):
            pos_valid_classes[i] = [x for x in classes if all(x.number_valid(t[i]) for t in other_tickets)]
        removed_classes = []
        while any(len(x) != 1 for x in pos_valid_classes.values()):
            min_i, min_classes = sorted([(x, y) for x, y in pos_valid_classes.items() if y[0] not in removed_classes],
                                        key=lambda x: len(x[1]))[0]
            if len(min_classes) != 1:
                raise AttributeError("Currently there is not a single position with just a single rule. "
                                     f"Cant work like that. Current min is {len(min_classes)}")
            min_classes = min_classes[0]
            for i in (x for x in pos_valid_classes.keys() if x != min_i):
                try:
                    pos_valid_classes[i].remove(min_classes)
                except ValueError:
                    pass
            removed_classes.append(min_classes)
        if any(not x[0].number_valid(own_ticket[i]) for i, x in pos_valid_classes.items()):
            return f"Your own ticket is invalid. Your ticket: {', '.join(str(x) for x in own_ticket)}", None
        result = 1
        for i in (x for x in pos_valid_classes.keys() if pos_valid_classes[x][0].get_name().startswith(return_fields)):
            result *= own_ticket[i]
        log.append(f"Your ticket:")
        for i, v in enumerate(own_ticket):
            log.append(f"  {pos_valid_classes[i][0]}: {v}")
        log.append(f"Searching for {return_fields} fields on your ticket")
        log.append(f"Multiplication results in {result}")
        return "\n".join(str(x) for x in log), result

    @staticmethod
    def _parse_data(data: List[str]):
        classes = []
        i = 0
        while i < len(data):
            line = data[i]
            i += 1
            if len(line) <= 0:
                break
            line = line.split(":")
            classes.append(Class(name=line[0].strip(), ranges=line[1].strip()))

        i += 1
        my_ticket = [int(x.strip()) for x in data[i].strip().split(",")]

        other_tickets = []
        i += 3
        while i < len(data):
            other_tickets.append([int(x.strip()) for x in data[i].strip().split(",")])
            i += 1

        return classes, my_ticket, other_tickets


class Class:
    def __init__(self, name: str, ranges: str):
        self._name = name
        self._min_max = []
        for min_max in ranges.split("or"):
            min_max = min_max.strip().split("-")
            min_max = (int(min_max[0]), int(min_max[1]))
            self._min_max.append((min(min_max), max(min_max)))

    def number_valid(self, value: int):
        return any(x[0] <= value <= x[1] for x in self._min_max)

    def get_name(self):
        return self._name

    def __str__(self):
        return self.get_name()

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.get_name()}: {', '.join(f'{x}-{y}' for x, y in self._min_max)}>"
