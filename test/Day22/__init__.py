import importlib
import os

_dirname = os.path.basename(os.path.dirname(__file__))

TheDay = getattr(importlib.import_module(f"AoC2020.{_dirname}"), _dirname)

INPUT_1 = [
    "Player 1:",
    "9",
    "2",
    "6",
    "3",
    "1",
    "",
    "Player 2:",
    "5",
    "8",
    "4",
    "7",
    "10"
]

RESULT_1 = 306
RESULT_2 = 291

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in INPUT_1), "utf-8"))


class TestDay(TheDay):
    pass
