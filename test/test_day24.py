from test.test_numpy import NUMPY_INSTALLED

if NUMPY_INSTALLED:
    from AoC.Day import StarTask
    from test import Day24 as TestDay

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


    def test_floor_colors():
        from AoC2020.Day24.Floor import Colors, COLOR_WHITE, COLOR_BLACK
        assert Colors.by_name(name=COLOR_WHITE.get_name()) == COLOR_WHITE
        assert Colors.by_name(name=COLOR_BLACK.get_name()) == COLOR_BLACK
        assert Colors.by_value(val=COLOR_WHITE.get_value()) == COLOR_WHITE
        assert Colors.by_value(val=COLOR_BLACK.get_value()) == COLOR_BLACK
