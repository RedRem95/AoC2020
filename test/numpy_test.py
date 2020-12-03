import pytest

NUMPY_INSTALLED = False
try:
    import numpy

    NUMPY_INSTALLED = True
except (ImportError, ModuleNotFoundError):
    with pytest.raises(SystemExit):
        import AoC.Day

        _ = AoC.Day.StarTask.Task01.name
