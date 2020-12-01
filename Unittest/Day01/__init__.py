import os
import json
import unittest

TEST_INPUT = [1721, 979, 366, 299, 675, 1456]
RESULT_1 = 514579
RESULT_2 = 241861950
TARGET = 2020

with open(os.path.join(os.path.dirname(__file__), "input_1.txt"), "wb") as f_out:
    f_out.write(bytes("\n".join(str(x) for x in TEST_INPUT), "utf-8"))

with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as f_out:
    json.dump({"target": 2020}, f_out)
