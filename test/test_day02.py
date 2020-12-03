from test.numpy_test import NUMPY_INSTALLED

if NUMPY_INSTALLED:
    from AoC.Day import StarTask
    from test import Day02 as TestDay

    _testDay = TestDay.TestDay()


    def test_task01():
        log, result = _testDay.run(task=StarTask.Task01)
        assert result == TestDay.RESULT_1


    def test_task02():
        log, result = _testDay.run(task=StarTask.Task02)
        assert result == TestDay.RESULT_2
