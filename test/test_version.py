import version
from test.numpy_test import NUMPY_INSTALLED

if NUMPY_INSTALLED:
    from AoC.Day import Day

    VERSION_PATTERN = "0.{day_number}.0-{day}"
    last_day = [x for x in Day.iterate_days()][-1]
    last_day_number = last_day.get_day()
    last_day_name = last_day.get_name()
    expected_version = VERSION_PATTERN.format(day_number=last_day_number, day=last_day_name)
else:
    expected_version = version.__VERSION


def test_version():
    assert str(version.get_version()) == expected_version
