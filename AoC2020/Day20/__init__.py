from typing import Tuple, List, Optional, Iterable

import numpy as np

from AoC.Day import Day, StarTask
from AoC2020.Day20.Image import Tile, SquareImageArray, replace_pattern


class Day20(Day):

    def __init__(self):
        super().__init__()
        self._sia: Optional[SquareImageArray] = None

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        tiles: List[Tile] = []
        current_tile: List[str] = []
        for line in [x.strip() for x in str(raw_input, "utf-8").strip().split("\n")]:
            if len(line) <= 0:
                if len(current_tile) > 0:
                    tiles.append(Tile.parse(data=current_tile))
                current_tile = []
            else:
                current_tile.append(line)
        if len(current_tile) > 0:
            tiles.append(Tile.parse(data=current_tile))
            str(tiles[-1])

        return tiles

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(tiles=self.get_input(task=task))
        if task == StarTask.Task02:
            return self._run02(tiles=self.get_input(task=task), sea_monster=self.get_day_config()["sea_monster"])
        return "", None

    def _get_sia(self, tiles: Iterable[Tile]) -> SquareImageArray:
        if self._sia is None:
            self._sia = SquareImageArray(tiles=tiles)
        return self._sia

    def _run01(self, tiles: List[Tile]) -> Tuple[str, object]:
        sia = self._get_sia(tiles=tiles)

        sia_matrix = sia.to_id_matrix()
        r = sia_matrix[0, 0] * sia_matrix[0, -1] * sia_matrix[-1, 0] * sia_matrix[-1, -1]

        log = [f"Created Square Image Array from {len(tiles)} tiles",
               f"Square image has {sia.get_edge_len()}x{sia.get_edge_len()}",
               f"Resulting image consists of ids:",
               str(sia)]

        return "\n".join(str(x) for x in log), r

    def _run02(self, tiles: List[Tile], sea_monster: List[str]) -> Tuple[str, object]:
        sia = self._get_sia(tiles=tiles)

        sea_monster = np.array([list(x) for x in sea_monster])

        for image in Tile.get_rotations_flips(data=sia.to_image()):
            before = len(np.where(image == "#")[0])
            times = replace_pattern(original=image, pattern=sea_monster, old_element="#", new_element="X")
            after = len(np.where(image == "#")[0])
            if after != before:
                sea_monster_rep = ["".join(y for y in x) for x in sea_monster]
                sea_monster_roof = f"  |-{'-' * max(len(x) for x in sea_monster_rep)}-|  "
                sea_monster_template = '  | {x:%ss} |  ' % max(len(x) for x in sea_monster_rep)
                log = [f"Found {times} sea monsters",
                       "A sea monster looks like:",
                       sea_monster_roof,
                       "\n".join(sea_monster_template.format(x=x) for x in sea_monster_rep),
                       sea_monster_roof,
                       "so cute *v*",
                       "",
                       f"Before we thought there was a roughness of {before}",
                       f"Now we know the roughness is {after}"]
                return "\n".join(log), after

        return "Didnt find any sea monster", len(np.where(sia.to_image() == "#")[0])
