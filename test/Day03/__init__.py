import json
import os

from AoC2020.Day03 import Day03

TEST_INPUT = ["..##.......",
              "#...#...#..",
              ".#....#..#.",
              "..#.#...#.#",
              ".#...##..#.",
              "..#.##.....",
              ".#.#.#....#",
              ".#........#",
              "#.##...#...",
              "#...##....#",
              ".#..#...#.#"
              ]
RESULT_1 = 7
RESULT_2 = 336
CONFIGS = {
    "Task01": [
        {"left": 3, "down": 1}
    ],
    "Task02": [
        {"left": 1, "down": 1},
        {"left": 3, "down": 1},
        {"left": 5, "down": 1},
        {"left": 7, "down": 1},
        {"left": 1, "down": 2}
    ]
}

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT), "utf-8"))

with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f_out:
    json.dump(CONFIGS, f_out)


class TestDay(Day03):

    def __init__(self):
        super().__init__()

    def get__file__(self) -> str:
        return __file__
