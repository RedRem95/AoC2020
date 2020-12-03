import pytest

NUMPY_INSTALLED = False
try:
    import numpy

    NUMPY_INSTALLED = True
except (ImportError, ModuleNotFoundError):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        import AoC.Day

        _ = AoC.Day.StarTask.Task01.name
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1
