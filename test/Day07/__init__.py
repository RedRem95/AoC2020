import json
import os
from typing import Tuple

from AoC.Day import StarTask
from AoC2020.Day07 import Day07 as TheDay

TEST_INPUT_1 = [
    "light red bags contain 1 bright white bag, 2 muted yellow bags.",
    "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
    "bright white bags contain 1 shiny gold bag.",
    "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
    "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
    "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
    "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
    "faded blue bags contain no other bags.",
    "dotted black bags contain no other bags."
]

TEST_INPUT_2 = [
    "shiny gold bags contain 2 dark red bags.",
    "dark red bags contain 2 dark orange bags.",
    "dark orange bags contain 2 dark yellow bags.",
    "dark yellow bags contain 2 dark green bags.",
    "dark green bags contain 2 dark blue bags.",
    "dark blue bags contain 2 dark violet bags.",
    "dark violet bags contain no other bags."
]

config = {
    "own_color": "shiny gold"
}

RESULT_1 = 4
RESULT_2_1 = 32
RESULT_2 = 126

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT_1), "utf-8"))

with open(os.path.join(os.path.dirname(__file__), "input_2.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT_2), "utf-8"))

with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f_out:
    json.dump(obj=config, fp=f_out)


class TestDay(TheDay):

    def run(self, task: StarTask) -> Tuple[str, object]:
        ret = super().run(task)
        if task == StarTask.Task02:
            _ = self._run02(task=StarTask.Task02)
            ret = (_[0], (ret[1], _[1]))
        return ret

    def get__file__(self) -> str:
        return __file__
