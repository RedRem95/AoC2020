from AoC2020.Day17.Dimensions import GameOfStates, ItsAlive, ItsDead
from test.test_numpy import NUMPY_INSTALLED

if NUMPY_INSTALLED:
    from AoC.Day import StarTask
    from test import Day17 as TestDay

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


    def test_dimension_str():
        init_state = [["#", "."], [".", "#"]]
        gos = GameOfStates(initial_plane=init_state, dimensions=2,
                           rules=[ItsAlive(), ItsDead()], interesting_states=None)
        assert str(gos) == "\n".join("".join(x) for x in init_state)
