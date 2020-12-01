import unittest
from AoC2020.Day01 import Day01
from AoC.Day import StarTask
from Unittest.Day01 import RESULT_1, RESULT_2


class TestDay01(Day01):

    def __init__(self):
        super().__init__()

    def get__file__(self) -> str:
        return __file__


class Test(unittest.TestCase):

    def __init__(self, methodName: str = None) -> None:
        if methodName is None:
            super().__init__()
        else:
            super().__init__(methodName)
        self._testDay = TestDay01()

    def testTask01(self):
        log, result = self._testDay.run(task=StarTask.Task01)
        self.assertEqual(result, RESULT_1, msg="Result for task 1 did not match")

    def testTask02(self):
        log, result = self._testDay.run(task=StarTask.Task02)
        self.assertEqual(result, RESULT_2, msg="Result for task 2 did not match")
