import json
import os

from AoC2020.Day12 import Day12 as TheDay

TEST_INPUT_1 = [
    "F10",
    "N3",
    "F7",
    "R90",
    "F11"
]

CONFIG = {
    "Task01": [
        1,
        0
    ],
    "Task02": [
        10,
        1
    ]
}

RESULT_1 = 25
RESULT_2 = 286

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT_1), "utf-8"))

with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f_out:
    json.dump(obj=CONFIG, fp=f_out)


class TestDay(TheDay):

    def get__file__(self) -> str:
        return __file__
