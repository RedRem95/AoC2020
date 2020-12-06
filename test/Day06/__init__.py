import os

from AoC2020.Day06 import Day06 as TheDay

TEST_INPUT_1 = [
    "abc",
    "",
    "a",
    "b",
    "c",
    "",
    "ab",
    "ac",
    "",
    "a",
    "a",
    "a",
    "a",
    "",
    "b",
]

RESULT_1 = 11
RESULT_2 = 6

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT_1), "utf-8"))


class TestDay(TheDay):

    def get__file__(self) -> str:
        return __file__
