import json
import os
from typing import Tuple, List

from AoC2020.Day15 import Day15 as TheDay

TEST_INPUT = [
    (["0,3,6"], 436, 175594),
    (["1,3,2"], 1, 2578),
    (["2,1,3"], 10, 3544142),
    (["1,2,3"], 27, 261214),
    (["2,3,1"], 78, 6895259),
    (["3,2,1"], 438, 18),
    (["3,1,2"], 1836, 362)
]

CONFIG = {
    "Task01": 2020,
    "Task02": 30000000
}

with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f_out:
    json.dump(obj=CONFIG, fp=f_out)

TestDays: List[Tuple[TheDay, int, int]] = []

for data in TEST_INPUT:
    with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
        f_out.write(bytes("\n".join(str(x) for x in data[0]), "utf-8"))


    class _TestDay(TheDay):

        def get__file__(self) -> str:
            return __file__


    TestDays.append((_TestDay(), data[1], data[2]))
