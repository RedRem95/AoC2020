import os

from AoC2020.Day08 import Day08 as TheDay

TEST_INPUT = [
    "nop +0",
    "acc +1",
    "jmp +4",
    "acc +3",
    "jmp -3",
    "acc -99",
    "acc +1",
    "jmp -4",
    "acc +6"
]

RESULT_1 = 5
RESULT_2 = 8

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT), "utf-8"))


class TestDay(TheDay):

    def get__file__(self) -> str:
        return __file__
