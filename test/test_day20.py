from test.test_numpy import NUMPY_INSTALLED

if NUMPY_INSTALLED:
    from AoC.Day import StarTask
    from test import Day20 as TestDay

    _testDay = TestDay.TestDay()


    def test_task01():
        log, result = _testDay.run(task=StarTask.Task01)
        assert result == TestDay.RESULT_1


    def test_task02():
        log, result = _testDay.run(task=StarTask.Task02)
        assert result == TestDay.RESULT_2


    def test_none():
        # noinspection PyTypeChecker
        log, result = _testDay.run(task=None)
        assert result is None
