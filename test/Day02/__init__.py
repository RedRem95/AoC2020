import os

from AoC2020.Day02 import Day02

TEST_INPUT = ["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc6"]
RESULT_1 = 2
RESULT_2 = 1

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT), "utf-8"))


class TestDay(Day02):

    def __init__(self):
        super().__init__()

    def get__file__(self) -> str:
        return __file__
