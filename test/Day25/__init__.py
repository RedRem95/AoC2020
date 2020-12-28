import importlib
import json
import os

_dirname = os.path.basename(os.path.dirname(__file__))

TheDay = getattr(importlib.import_module(f"AoC2020.{_dirname}"), _dirname)

INPUT_1 = [
    5764801,
    17807724
]

CONFIG = {
    "subject_number": 7,
    "divisor": 20201227
}

RESULT_1 = 14897079
RESULT_2 = None

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in INPUT_1), "utf-8"))

with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f_out:
    json.dump(obj=CONFIG, fp=f_out)


class TestDay(TheDay):
    pass
