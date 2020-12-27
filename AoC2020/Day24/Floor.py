from copy import copy
from typing import Dict, Tuple, List, Optional, Generator

from AoC2020.Day17.GameOfStates import GameOfStates, State, StateRule

_MOVEMENT = {
    "e": (1, 0),
    "se": (0, -1),
    "sw": (-1, -1),
    "w": (-1, 0),
    "nw": (0, 1),
    "ne": (1, 1)
}


class Colors(State[int]):
    _created_states: List["Colors"] = []

    def __init__(self, name: str, value: int):
        self._value = value
        self._name = name
        self.__class__._created_states.append(self)

    @classmethod
    def get_default_state(cls) -> "Colors":
        return COLOR_WHITE

    @classmethod
    def iterate_states(cls) -> Generator["Colors", "Colors", None]:
        for i in cls._created_states:
            yield i

    def get_name(self) -> str:
        return self._name

    def get_value(self) -> int:
        return self._value

    def __str__(self):
        return self.get_value()

    def switch(self) -> "Colors":
        if self == COLOR_WHITE:
            return COLOR_BLACK
        if self == COLOR_BLACK:
            return COLOR_WHITE
        return COLOR_WHITE


COLOR_WHITE = Colors("White", 1)
COLOR_BLACK = Colors("Black", 0)


class Floor(GameOfStates):

    def __init__(self, default_color: Colors = COLOR_WHITE, starting_tile: Tuple[int, int] = (0, 0)):

        super().__init__([], [BlackToWhite(), WhiteToBlack()], dimensions=2, used_state_type=Colors)
        self._floor: Dict[Tuple[int, int], Colors] = {}
        self._default_color: Colors = default_color
        self._starting_tile = starting_tile

    def _get_adjacent(self, *coordinates: int) -> List[Tuple[int, ...]]:
        ret = []
        for movement in _MOVEMENT.values():
            ret.append((coordinates[0] + movement[0], coordinates[1] + movement[1]))
        return ret

    def get_at(self, *coordinates: int) -> Colors:
        return self._floor.get(coordinates, self._default_color)

    def _get_data(self):
        return self._floor

    def _set_data(self, data: Dict[Tuple[int, ...], Optional[Colors]]):
        self._floor = data

    def parse(self, tile_identifications: List[str]):

        for tile in tile_identifications:
            i = 0
            current_tile = copy(self._starting_tile)
            while i < len(tile):
                j = 1
                while True:
                    try:
                        movement = _MOVEMENT[tile[i:i + j]]
                        current_tile = current_tile[0] + movement[0], current_tile[1] + movement[1]
                        break
                    except KeyError:
                        pass
                    j += 1
                i += j
            self._floor[current_tile] = self._floor.get(current_tile, self._default_color).switch()

    def count(self, target_state: Colors):
        return super().count(target_state)


class BlackToWhite(StateRule):

    def apply(self, me: Colors, adjacent: List[Colors]) -> Optional[Colors]:
        if me == COLOR_BLACK:
            black_friends = sum(x == COLOR_BLACK for x in adjacent)
            if black_friends == 0 or black_friends > 2:
                return COLOR_WHITE
            else:
                return COLOR_BLACK
        return None


class WhiteToBlack(StateRule):

    def apply(self, me: Colors, adjacent: List[Colors]) -> Optional[Colors]:
        if me == COLOR_WHITE:
            black_friends = sum(x == COLOR_BLACK for x in adjacent)
            if black_friends == 2:
                return COLOR_BLACK
            else:
                return COLOR_WHITE
        return None
