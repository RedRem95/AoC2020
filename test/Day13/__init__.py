import os

from AoC2020.Day13 import Day13 as TheDay

TEST_INPUT_1 = [
    "939",
    "7,13,x,x,59,x,31,19"
]

RESULT_1 = 295
RESULT_2 = None

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT_1), "utf-8"))


class TestDay(TheDay):

    def get__file__(self) -> str:
        return __file__
