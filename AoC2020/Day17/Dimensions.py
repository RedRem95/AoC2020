import itertools
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, List, Union, Tuple, Dict

import numpy as np


class State(Enum):
    ACTIVE = "#",
    INACTIVE = "."

    @classmethod
    def by_value(cls, val: str) -> Optional["State"]:
        for i in cls:
            if val == str(i):
                return i
        return None

    def __str__(self):
        return str(self.value[0] if hasattr(self.value, "__iter__") else self.value)


class StateRule(ABC):
    @abstractmethod
    def apply(self, me: State, adjacent: List[State]) -> Optional[State]:
        pass


class GameOfStates:

    def __init__(self,
                 initial_plane: List[List[Union[str, State]]],
                 rules: List[StateRule],
                 dimensions: int = 3,
                 interesting_states: Optional[List[State]] = None):
        self._data: Dict[Tuple[int, ...], Optional[State]] = {}
        zero_dimensions = [0] * (dimensions - 2)
        self._rules = [x for x in rules]
        self._dimensions = dimensions
        self._interesting_states = interesting_states
        for y, line in enumerate(initial_plane):
            for x, element in enumerate(line):
                state = State.by_value(str(element))
                if state is not None and self._is_state_interesting(state):
                    self._data[tuple([x, y] + zero_dimensions)] = State.by_value(str(element))

    def _is_state_interesting(self, state: State):
        if self._interesting_states is None:
            return True
        return state in self._interesting_states

    def _get_adjacent(self, *coordinates: int) -> List[Tuple[int, ...]]:
        ret: List[Tuple[int, ...]] = []
        for delta in itertools.product(range(-1, 2, 1), repeat=len(coordinates)):
            if all(d == 0 for d in delta):
                continue
            ret.append(tuple(c + d for c, d in zip(coordinates, delta)))
        return ret

    def get_at(self, *coordinates: int) -> State:
        return self._data.get(coordinates, State.INACTIVE)

    def next(self):
        next_stage: Dict[Tuple[int, ...], Optional[State]] = {}

        work_coordinates = set()
        work_coordinates.add(tuple([0] * self._dimensions))
        for c in self._data.keys():
            if len(c) != self._dimensions:
                raise IndexError(f"coordinate-dimension does not math set dimension: {c}->{len(c)}!={self._dimensions}")
            work_coordinates.add(c)
            for a in self._get_adjacent(*c):
                if len(a) != self._dimensions:
                    raise IndexError(f"coordinate-dimension does not math set dimension: {a}->{len(a)}!="
                                     f"{self._dimensions}")
                work_coordinates.add(a)

        for coordinate in work_coordinates:
            adjacent_coordinates = self._get_adjacent(*coordinate)
            me = self.get_at(*coordinate)
            adjacent = [self.get_at(*c) for c in adjacent_coordinates]
            r = None
            for rule in self._rules:
                r = rule.apply(me=me, adjacent=adjacent)
                if r is not None:
                    break
            if self._is_state_interesting(r):
                next_stage[coordinate] = r

        something_changed = self.compare_stages(s1=self._data, s2=next_stage)
        self._data = next_stage
        return something_changed

    @staticmethod
    def compare_stages(s1: Dict[Tuple[int, ...], Optional[State]], s2: Dict[Tuple[int, ...], Optional[State]]):
        for coordinate in set([x for x in s1.keys()] + [x for x in s2.keys()]):
            if s1.get(coordinate, None) != s2.get(coordinate, None):
                return False
        return True

    def count(self, target_state: State):
        return sum(1 if v == target_state else 0 for v in self._data.values())

    def __str__(self):
        z_dimensions = self._dimensions - 2
        if z_dimensions > 0:
            if z_dimensions > 1:
                z_template = "z_{i}={z}"
            else:
                z_template = "z={z}"
        else:
            z_template = None
        all_coordinates = np.array([x for x in self._data.keys()])
        min_coordinates = np.min(all_coordinates, axis=0)
        max_coordinates = np.max(all_coordinates, axis=0)

        ret = []

        all_zs = itertools.product(*[range(mi, ma + 1, 1) for mi, ma in zip(min_coordinates[2:], max_coordinates[2:])])

        for zs in all_zs:
            if len(ret) > 0:
                ret.append("")
            if z_template is not None:
                ret.append(", ".join(z_template.format(i=i, z=z) for i, z in enumerate(zs)))
            line = []
            for y in range(min_coordinates[1], max_coordinates[1] + 1, 1):
                for x in range(min_coordinates[0], max_coordinates[0] + 1, 1):
                    line.append(str(self.get_at(*tuple((x, y) + zs))))
                ret.append("".join(line))
                line = []

        return "\n".join(ret)

    def get_dimensionality(self):
        return self._dimensions


class ItsAlive(StateRule):
    def apply(self, me: State, adjacent: List[State]) -> Optional[State]:
        if me == State.ACTIVE:
            if sum(1 if a == State.ACTIVE else 0 for a in adjacent) in (2, 3):
                return State.ACTIVE
            else:
                return State.INACTIVE
        return None


class ItsDead(StateRule):
    def apply(self, me: State, adjacent: List[State]) -> Optional[State]:
        if me == State.INACTIVE:
            if sum(1 if a == State.ACTIVE else 0 for a in adjacent) == 3:
                return State.ACTIVE
            else:
                return State.INACTIVE
        return None
