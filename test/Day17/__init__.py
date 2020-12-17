import json
import os

from AoC2020.Day17 import Day17 as TheDay

CONFIG = {
    "Task01": {
        "steps": 6,
        "dimensions": 3
    },
    "Task02": {
        "steps": 6,
        "dimensions": 4
    }
}

INPUT_1 = [
    ".#.",
    "..#",
    "###"
]

RESULT_1 = 112
RESULT_2 = 848

with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f_out:
    json.dump(obj=CONFIG, fp=f_out)

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in INPUT_1), "utf-8"))


class TestDay(TheDay):
    pass
