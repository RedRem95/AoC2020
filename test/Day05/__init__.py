import os

from AoC2020.Day05 import Day05

TEST_INPUT_1 = [
    "BFFFBBFRRR",  # 567
    "FFFBBBFRRR",  # 119
    "BBFFBBFRLL",  # 820
    "FBFBBFFRLR"  # 357
]

RESULT_1 = 820
RESULT_2 = set(range(119, 820, 1))

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT_1), "utf-8"))


class TestDay(Day05):

    def get__file__(self) -> str:
        return __file__
