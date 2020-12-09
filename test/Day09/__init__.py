import json
import os

from AoC2020.Day09 import Day09 as TheDay

TEST_INPUT_1 = [
    35,
    20,
    15,
    25,
    47,
    40,
    62,
    55,
    65,
    95,
    102,
    117,
    150,
    182,
    127,
    219,
    299,
    277,
    309,
    576,
]

CONFIG = {
    "preamble_length": 5
}

RESULT_1 = 127
RESULT_2 = 62

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT_1), "utf-8"))

with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f_out:
    json.dump(obj=CONFIG, fp=f_out)


class TestDay(TheDay):

    def get__file__(self) -> str:
        return __file__
