from test import Day01
from AoC.Day import StarTask

_testDay = Day01.TestDay01()


def test_task01():
    log, result = _testDay.run(task=StarTask.Task01)
    assert Day01.RESULT_1 == result


def test_task02():
    log, result = _testDay.run(task=StarTask.Task02)
    assert Day01.RESULT_2 == result
