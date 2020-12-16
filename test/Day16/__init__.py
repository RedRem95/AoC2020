import json
import os
from random import choice

from AoC2020.Day16 import Day16 as TheDay

__own_ticket = choice([("row", 11), ("class", 12), ("seat", 13)])

CONFIG = {
    "interesting_fields": __own_ticket[0]
}

INPUT_1 = [
    "class: 1-3 or 5-7",
    "row: 6-11 or 33-44",
    "seat: 13-40 or 45-50",
    "",
    "your ticket:",
    "7,1,14",
    "",
    "nearby tickets:",
    "7,3,47",
    "40,4,50",
    "55,2,20",
    "38,6,12"
]

INPUT_2 = [
    "class: 0-1 or 4-19",
    "row: 0-5 or 8-19",
    "seat: 0-13 or 16-19",
    "",
    "your ticket:",
    "11,12,13",
    "",
    "nearby tickets:",
    "3,9,18",
    "15,1,5",
    "5,14,9"
]

RESULT_1 = 71
RESULT_2 = __own_ticket[1]

with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f_out:
    json.dump(obj=CONFIG, fp=f_out)

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in INPUT_1), "utf-8"))

with open(os.path.join(os.path.dirname(__file__), "input_2.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in INPUT_2), "utf-8"))


class TestDay(TheDay):
    pass
