from typing import Tuple, Callable, Dict

import numpy as np


class Ship:
    def __init__(self, pos: Tuple[int, int] = (0, 0), waypoint: Tuple[int, int] = (1, 0), waypoint_mode: bool = False):
        self._waypoint_mode = waypoint_mode
        self._pos = np.array(pos)
        self._start = pos
        self._waypoint: np.ndarray = np.array(waypoint)
        self._west = np.array([-1, 0])
        self._east = np.array([1, 0])
        self._south = np.array([0, -1])
        self._north = np.array([0, 1])

        o_move: Callable[[float, np.ndarray], None] = self._move_waypoint if waypoint_mode else self._move

        self._instructions: Dict[str, Callable[[float], None]] = {
            "N": lambda d: o_move(d, self._north),
            "S": lambda d: o_move(d, self._south),
            "E": lambda d: o_move(d, self._east),
            "W": lambda d: o_move(d, self._west),
            "R": self.right,
            "L": self.left,
            "F": lambda d: self._move(orientation=self._waypoint, distance=d),
        }

    @staticmethod
    def _absolute_move(pos: np.ndarray, move: np.ndarray):
        return pos + move

    def _move(self, distance: float, orientation: np.ndarray):
        self._pos = self._absolute_move(move=orientation * distance, pos=self._pos)

    def _move_waypoint(self, distance: float, orientation: np.ndarray):
        self._waypoint = self._absolute_move(move=orientation * distance, pos=self._waypoint)

    def in_waypoint_mode(self) -> bool:
        return self._waypoint_mode

    def get_pos(self) -> Tuple[float, float]:
        return self._pos[0], self._pos[1]

    def get_waypoint(self) -> Tuple[float, float]:
        return self._waypoint[0], self._waypoint[1]

    @staticmethod
    def manhattan_dist(p1: Tuple[float, float], p2: Tuple[float, float]):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def manhattan_from_start(self):
        return self.manhattan_dist(p1=self._start, p2=self.get_pos())

    def left(self, degree: float = 90):
        theta = np.radians(degree)
        c, s = np.cos(theta), np.sin(theta)
        rot = np.array(((c, -s), (s, c)))
        self._waypoint = np.round(np.dot(rot, self._waypoint), decimals=5)

    def right(self, degree: float = 90):
        self.left(degree=-degree)

    def parse(self, instruction: str) -> bool:
        for i in range(1, len(instruction), 1):
            try:
                value = int(instruction[i:])
                if instruction[:i] in self._instructions:
                    self._instructions[instruction[:i]](value)
                    return True
            except ValueError:
                pass
        return False
