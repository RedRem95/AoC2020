import itertools
from abc import ABC, abstractmethod
from typing import Optional, List, Union, Tuple, Dict, TypeVar, Type, Generic, Generator

import numpy as np

T = TypeVar("T")


class State(ABC, Generic[T]):

    @classmethod
    def by_value(cls, val: T) -> Optional["State"]:
        for i in cls.iterate_states():
            if val == i.get_value():
                return i
        return None

    @classmethod
    def by_name(cls, name: str) -> Optional["State"]:
        for i in cls.iterate_states():
            if name == i.get_name():
                return i
        return None

    @classmethod
    @abstractmethod
    def get_default_state(cls) -> "State":
        pass

    @classmethod
    @abstractmethod
    def iterate_states(cls) -> Generator["State", "State", None]:
        pass

    @abstractmethod
    def get_value(self) -> T:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}<name: {self.get_name()}, value: {self.get_value()}>"


class DefaultState(State[str]):
    _created_states: List["DefaultState"] = []

    def __init__(self, name: str, value: str):
        self._value = value
        self._name = name
        self.__class__._created_states.append(self)

    @classmethod
    def get_default_state(cls) -> "DefaultState":
        return INACTIVE

    @classmethod
    def iterate_states(cls) -> Generator["DefaultState", "DefaultState", None]:
        for i in cls._created_states:
            yield i

    def get_name(self) -> str:
        return self._name

    def get_value(self) -> str:
        return self._value

    def __str__(self):
        return self.get_value()


ACTIVE = DefaultState(name="ACTIVE", value="#")
INACTIVE = DefaultState(name="INACTIVE", value=".")


class StateRule(ABC):
    @abstractmethod
    def apply(self, me: State, adjacent: List[State]) -> Optional[State]:
        pass


class GameOfStates:

    def __init__(self,
                 initial_plane: List[List[Union[str, State]]],
                 rules: List[StateRule],
                 dimensions: int = 3,
                 interesting_states: Optional[List[State]] = None,
                 used_state_type: Type[State] = DefaultState):
        self._used_state_type = used_state_type
        self._data: Dict[Tuple[int, ...], Optional[State]] = {}
        zero_dimensions = [0] * (dimensions - 2)
        self._rules = [x for x in rules]
        self._dimensions = dimensions
        self._interesting_states = interesting_states
        for y, line in enumerate(initial_plane):
            for x, element in enumerate(line):
                state = used_state_type.by_value(str(element))
                if state is not None and self._is_state_interesting(state):
                    self._data[tuple([x, y] + zero_dimensions)] = used_state_type.by_value(str(element))

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
        return self._data.get(coordinates, self._used_state_type.get_default_state())

    def _get_data(self):
        return self._data

    def _set_data(self, data: Dict[Tuple[int, ...], Optional[State]]):
        self._data = data

    def next(self):
        next_stage: Dict[Tuple[int, ...], Optional[State]] = {}

        work_coordinates = set()
        work_coordinates.add(tuple([0] * self._dimensions))
        for c in self._get_data().keys():
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

        something_changed = self.compare_stages(s1=self._get_data(), s2=next_stage)
        self._set_data(next_stage)
        return something_changed

    @staticmethod
    def compare_stages(s1: Dict[Tuple[int, ...], Optional[State]], s2: Dict[Tuple[int, ...], Optional[State]]):
        for coordinate in set([x for x in s1.keys()] + [x for x in s2.keys()]):
            if s1.get(coordinate, None) != s2.get(coordinate, None):
                return False
        return True

    def count(self, target_state: State):
        return sum(1 if v == target_state else 0 for v in self._get_data().values())

    def __str__(self):
        z_dimensions = self._dimensions - 2
        if z_dimensions > 0:
            if z_dimensions > 1:
                z_template = "z_{i}={z}"
            else:
                z_template = "z={z}"
        else:
            z_template = None
        all_coordinates = np.array([x for x in self._get_data().keys()])
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
    def apply(self, me: DefaultState, adjacent: List[DefaultState]) -> Optional[DefaultState]:
        if me == ACTIVE:
            if sum(1 if a == ACTIVE else 0 for a in adjacent) in (2, 3):
                return ACTIVE
            else:
                return INACTIVE
        return None


class ItsDead(StateRule):
    def apply(self, me: DefaultState, adjacent: List[DefaultState]) -> Optional[DefaultState]:
        if me == INACTIVE:
            if sum(1 if a == ACTIVE else 0 for a in adjacent) == 3:
                return ACTIVE
            else:
                return INACTIVE
        return None
