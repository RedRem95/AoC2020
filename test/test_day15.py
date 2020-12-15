from test.test_numpy import NUMPY_INSTALLED

if NUMPY_INSTALLED:
    from AoC.Day import StarTask
    from test import Day15 as TestDay

    _testDays = TestDay.TestDays


    def test_task01():
        for i, (_testDay, r1, r2) in enumerate(_testDays):
            log, result = _testDay.run(task=StarTask.Task01)
            assert r1 == result, f"The {i + 1}. test input failed"


    def test_task02():
        for i, (_testDay, r1, r2) in enumerate(_testDays):
            log, result = _testDay.run(task=StarTask.Task02)
            assert r2 == result, f"The {i + 1}. test input failed"


    def test_none():
        for i, (_testDay, r1, r2) in enumerate(_testDays):
            # noinspection PyTypeChecker
            log, result = _testDay.run(task=None)
            assert result is None, f"The {i + 1}. test input failed"
