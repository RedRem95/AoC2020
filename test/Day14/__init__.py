import json
import os

from AoC2020.Day14 import Day14 as TheDay

TEST_INPUT_1 = [
    "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
    "mem[8] = 11",
    "mem[7] = 101",
    "mem[8] = 0",
]

TEST_INPUT_2 = [
    "mask = 000000000000000000000000000000X1001X",
    "mem[42] = 100",
    "mask = 00000000000000000000000000000000X0XX",
    "mem[26] = 1",
]

CONFIG = {
    "bit_length": 36
}

RESULT_1 = 165
RESULT_2 = 208

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT_1), "utf-8"))

with open(os.path.join(os.path.dirname(__file__), "input_2.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT_2), "utf-8"))

with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f_out:
    json.dump(obj=CONFIG, fp=f_out)


class TestDay(TheDay):

    def get__file__(self) -> str:
        return __file__
