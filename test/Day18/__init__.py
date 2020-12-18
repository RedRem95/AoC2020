import json
import os

from AoC2020.Day18 import Day18 as TheDay

CONFIG = {
    "Task02": ["+", "*"]
}

INPUT_1 = [
    "1 + (2 * 3) + (4 * (5 + 6))",
    "2 * 3 + (4 * 5)",
    "5 + (8 * 3 + 9 + 3 * 4 * 3)",
    "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",
    "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
]

RESULT_1 = 51 + 26 + 437 + 12240 + 13632
RESULT_2 = 51 + 46 + 1445 + 669060 + 23340

with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f_out:
    json.dump(obj=CONFIG, fp=f_out)

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in INPUT_1), "utf-8"))


class TestDay(TheDay):
    pass
