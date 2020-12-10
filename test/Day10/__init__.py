import os

from AoC2020.Day10 import Day10 as TheDay

TEST_INPUT_1 = [
    28,
    33,
    18,
    42,
    31,
    14,
    46,
    20,
    48,
    47,
    24,
    23,
    49,
    45,
    19,
    38,
    39,
    11,
    1,
    32,
    25,
    35,
    8,
    17,
    7,
    9,
    4,
    2,
    34,
    10,
    3
]

RESULT_1 = 220
RESULT_2 = 19208

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT_1), "utf-8"))


class TestDay(TheDay):

    def get__file__(self) -> str:
        return __file__
