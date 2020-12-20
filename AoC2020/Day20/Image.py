from copy import deepcopy
from typing import List, Iterable, Dict, Tuple, Set, Optional

import numpy as np


def is_square(m):
    tmp = len(m)
    return all(len(row) == tmp for row in m)


class Tile:

    def __init__(self, tile_id: int, tile_data: np.ndarray):
        self._data = tile_data
        self._tile_id = tile_id
        if not is_square(self._data):
            raise Exception("Produced image fragment is not square")

    @classmethod
    def parse(cls, data: List[str]):
        if not data[0].startswith("Tile"):
            raise Exception("First line must state ID")
        return Tile(tile_id=int(data[0][len("Title"):-1].strip()),
                    tile_data=np.array([[x for x in y] for y in data[1:]]))

    def get_upper_border(self):
        return self._data[0, :].flatten()

    def get_lower_border(self):
        return self._data[-1, :].flatten()

    def get_right_border(self):
        return self._data[:, -1].flatten()

    def get_left_border(self):
        return self._data[:, 0].flatten()

    def get_id(self) -> int:
        return self._tile_id

    def get_possible_tiles(self) -> Iterable["Tile"]:
        ret = [self]
        for k in range(0, 4, 1):
            rot_data = np.rot90(m=self._data, k=k, axes=(0, 1))
            for n_t in (Tile(tile_id=self.get_id(), tile_data=rot_data),
                        Tile(tile_id=self.get_id(), tile_data=np.flip(m=rot_data, axis=0)),
                        Tile(tile_id=self.get_id(), tile_data=np.flip(m=rot_data, axis=1)),
                        Tile(tile_id=self.get_id(), tile_data=np.flip(m=np.flip(m=rot_data, axis=0), axis=1))):
                if not any([np.all(n_t._data == x._data) for x in ret]):
                    ret.append(n_t)
        ret = []
        for rotations in self.get_rotations_flips(data=self._data):
            ret.append(Tile(tile_id=self.get_id(), tile_data=rotations))
        return ret

    @staticmethod
    def get_rotations_flips(data: np.ndarray) -> Iterable[np.ndarray]:
        ret = []
        for k in range(0, 4, 1):
            rot_data = np.rot90(m=data, k=k, axes=(0, 1))
            for n_t in (rot_data, np.flip(m=rot_data, axis=0), np.flip(m=rot_data, axis=1),
                        np.flip(m=np.flip(m=rot_data, axis=0), axis=1)):
                if len(ret) <= 0 or not any([np.all(n_t == x) for x in ret]):
                    ret.append(n_t)
        return ret

    def to_image(self) -> List[str]:
        return ["".join(str(x) for x in y) for y in self._data]

    def __str__(self):
        image = "\n".join(self.to_image())
        return f"Tile {self.get_id()}:\n{image}"


class SquareImageArray:

    def __init__(self, tiles: Iterable[Tile]):
        self._raw: Dict[int, List[Tile]] = dict((x.get_id(), [y for y in x.get_possible_tiles()]) for x in tiles)
        self._edge_len = int(np.sqrt(len(self._raw)))
        if self._edge_len ** 2 != len(self._raw):
            raise Exception(f"Cant produce squared image from {len(self._raw)} images")
        self._fitted: List[List[Tuple[int, int]]] = self._fit()

    def get_edge_len(self):
        return self._edge_len

    def _fit(self, current: List[List[Tuple[int, int]]] = None) -> Optional[List[List[Tuple[int, int]]]]:

        if current is None:
            current = [[]]

        already_used: Set[int] = set()
        for line in current:
            for tile_ref in line:
                already_used.add(tile_ref[0])

        if len(already_used) >= len(self._raw):
            return current

        if len(current[-1]) >= self.get_edge_len():
            current.append([])

        check_left: Optional[Tile] = self._raw[current[-1][-1][0]][current[-1][-1][1]] if len(current[-1]) > 0 else None
        check_top: Optional[Tile] = None
        if len(current) > 1:
            if len(current[-2]) > len(current[-1]):
                check_top = self._raw[current[-2][len(current[-1])][0]][current[-2][len(current[-1])][1]]

        for possible_id in (x for x in self._raw.keys() if x not in already_used):
            for tile_id, tile in enumerate(self._raw[possible_id]):
                if check_left is not None and np.any(check_left.get_right_border() != tile.get_left_border()):
                    continue
                if check_top is not None and np.any(check_top.get_lower_border() != tile.get_upper_border()):
                    continue
                current_temp = deepcopy(current)
                current_temp[-1].append((possible_id, tile_id))
                fitted = self._fit(current=current_temp)
                if fitted is not None:
                    return fitted

        return None

    def to_image(self) -> np.ndarray:
        def cut_tile(_tile: List[str]) -> List[str]:
            return ["".join(x[1:-1]) for x in _tile[1:-1]]

        ret: List[List[str]] = []
        for line in self._fitted:
            tiles = [cut_tile(self._raw[x[0]][x[1]].to_image()) for x in line]
            line_len = 1
            for tile_line in range(max(len(i) for i in tiles)):
                ret.append(list("".join(t[tile_line] for t in tiles)))
                line_len = max(line_len, len(ret[-1]))
        return np.array(ret)

    def to_id_matrix(self) -> np.ndarray:
        return np.array([[x[0] for x in y] for y in self._fitted], dtype=int)

    def __str__(self):
        _matrix = self.to_id_matrix()
        template = "{x:%sd}" % len(str(np.max(_matrix)))
        return "\n".join(" ".join(template.format(x=i) for i in line) for line in _matrix)


def replace_pattern(original: np.ndarray, pattern: np.ndarray, old_element: object, new_element: object) -> int:
    indices_pattern = np.where(pattern == old_element)
    indices_pattern_relative = indices_pattern[0] - indices_pattern[0][0], indices_pattern[1] - indices_pattern[1][0]
    indices_original = np.where(original == old_element)
    replace_indices = ([], [])
    times_replaced = 0

    for place_y, place_x in zip(*indices_original):
        check_places = indices_pattern_relative[0] + place_y, indices_pattern_relative[1] + place_x
        try:
            if np.any(check_places[0] < 0) or np.any(check_places[1] < 0):
                raise IndexError
            if np.all(original[check_places] == old_element):
                replace_indices[0].extend(check_places[0])
                replace_indices[1].extend(check_places[1])
                times_replaced += 1

        except IndexError:
            continue

    original[replace_indices] = new_element

    return times_replaced
