import importlib
import json
import os

_dirname = os.path.basename(os.path.dirname(__file__))

TheDay = getattr(importlib.import_module(f"AoC2020.{_dirname}"), _dirname)

INPUT_1 = [
    "389125467"
]

CONFIG = {
    "Task01": {
        "rounds": 100,
        "target_amount": -1
    },
    "Task02": {
        "rounds": 10000000,
        "target_amount": 1000000
    }
}

RESULT_1 = 67384529
RESULT_2 = 149245887792

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in INPUT_1), "utf-8"))

with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f_out:
    json.dump(CONFIG, f_out)


class TestDay(TheDay):
    pass
