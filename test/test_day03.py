from AoC.Day import StarTask
from test import Day03 as TestDay

_testDay = TestDay.TestDay()


def test_task01():
    log, result = _testDay.run(task=StarTask.Task01)
    assert TestDay.RESULT_1 == result


def test_task02():
    log, result = _testDay.run(task=StarTask.Task02)
    assert TestDay.RESULT_2 == result
