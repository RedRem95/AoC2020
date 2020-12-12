import itertools
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, List, Dict, Iterable, Union, Tuple


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


class Rule(ABC):
    @abstractmethod
    def apply(self, me: Places, adjacent: List[Places]) -> Optional[Places]:
        pass


class Stage:

    def __init__(self, data: List[List[Union[Places, str]]], rules: Iterable[Rule]):
        self._data = [[Places.by_value(str(y)) for y in x] for x in data]
        self._rules = rules

    def count(self, seat_type: Places) -> int:
        return sum(sum(1 if y == seat_type else 0 for y in x) for x in self._data)

    def next(self) -> bool:
        new_stage: List[List["Places"]] = [[]]

        for y, line in enumerate(self._data):
            for x, seat in enumerate(line):
                adjacent = [self._data[_y][_x] for _x, _y in self._get_adjacent(x=x, y=y)]
                new_seat = None
                for rule in self._rules:
                    new_seat = rule.apply(me=seat, adjacent=adjacent)
                    if new_seat is not None:
                        break
                new_stage[-1].append(seat if new_seat is None else new_seat)
            new_stage.append([])

        new_stage = [x for x in new_stage if len(x) > 0]

        nothing_changed = self.compare_stages(self._data, new_stage)

        self._data = [[y for y in x] for x in new_stage]

        return not nothing_changed

    def find_stable(self, max_iterations: int = -1) -> Optional[int]:
        i = 0
        while self.next():
            i += 1
            if 0 < max_iterations < i:
                return None
        return i

    def _get_adjacent(self, x, y) -> List[Tuple[int, int]]:
        ret: List[Tuple[int, int]] = []
        for i, j in itertools.product(range(-1, 2, 1), repeat=2):
            if i == 0 and j == 0:
                continue
            try:
                _ = self._data[y+j][x+i]
                ret.append((x + i, y + j))
            except IndexError:
                pass
        return [t for t in ret if t[0] >= 0 and t[1] >= 0]

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

    def __str__(self):
        if self._data is None:
            return ""
        return "\n".join("".join(str(y) for y in x) for x in self._data)


class IH8PPL(Rule):

    def __init__(self, i_hate_so_many: int) -> None:
        super().__init__()
        self._i_hate_so_many = i_hate_so_many

    def apply(self, me: Places, adjacent: List[Places]) -> Optional[Places]:
        if me == Places.OCCUPIED and sum(1 if x == Places.OCCUPIED else 0 for x in adjacent) >= self._i_hate_so_many:
            return Places.EMPTY
        return None


class ItsFreeRealEstate(Rule):
    def apply(self, me: Places, adjacent: List[Places]) -> Optional[Places]:
        if me == Places.EMPTY and all(x in (Places.EMPTY, Places.FLOOR) for x in adjacent):
            return Places.OCCUPIED
        return None


class FloorIsFloor(Rule):
    def apply(self, me: Places, adjacent: List[Places]) -> Optional[Places]:
        if me == Places.FLOOR:
            return Places.FLOOR
        return None


class ViewingStage(Stage):
    def __init__(self, data: List[List[Union[Places, str]]], rules: Iterable[Rule]):
        super().__init__(data, rules)

    def _get_adjacent(self, x, y) -> List[Tuple[int, int]]:
        simple_adjacent = [(p[0] - x, p[1] - y) for p in super()._get_adjacent(x, y)]
        seeing_adjacent = []
        j = 1
        while len(simple_adjacent) > 0:
            for i in range(len(simple_adjacent) - 1, -1, -1):
                _x, _y = int(simple_adjacent[i][0] * j) + x, int(simple_adjacent[i][1] * j) + y
                try:
                    if _x < 0 or _y < 0:
                        raise IndexError("Cant wrap around here")
                    if self._data[_y][_x] != Places.FLOOR:
                        seeing_adjacent.append((_x, _y))
                        raise IndexError("No error but remove pls")
                except IndexError:
                    simple_adjacent.remove(simple_adjacent[i])
            j += 1
        return seeing_adjacent
