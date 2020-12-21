import importlib
import os

_dirname = os.path.basename(os.path.dirname(__file__))

TheDay = getattr(importlib.import_module(f"AoC2020.{_dirname}"), _dirname)

INPUT_1 = [
    "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
    "trh fvjkl sbzzf mxmxvkd (contains dairy)",
    "sqjhc fvjkl (contains soy)",
    "sqjhc mxmxvkd sbzzf (contains fish)"
]

RESULT_1 = 5
RESULT_2 = "mxmxvkd,sqjhc,fvjkl"

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in INPUT_1), "utf-8"))


class TestDay(TheDay):
    pass
