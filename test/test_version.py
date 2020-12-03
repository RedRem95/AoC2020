from AoC.Day import Day
from version import get_version as version

VERSION_PATTERN = "0.{day_number}.0-{day}"


def test_version():
    last_day = [x for x in Day.iterate_days()][-1]
    expected_version = VERSION_PATTERN.format(day_number=last_day.get_day(), day=last_day.get_name())
    assert expected_version == str(version())
