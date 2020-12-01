import os
import datetime

THIS_YEAR = int(os.environ.get("AOC_YEAR", datetime.datetime.now().year))


def __import_days():

    import re
    import importlib
    import os
    pattern = re.compile(r"Day[0-2][0-9]")
    import_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"AoC{THIS_YEAR}")
    for folder in (x for x in os.listdir(import_folder) if pattern.match(x)):
        folder_abs = os.path.join(import_folder, folder)
        if os.path.exists(folder_abs) and os.path.isdir(folder_abs) and os.path.exists(
                os.path.join(folder_abs, "__init__.py")):
            try:
                tmp = importlib.import_module(os.path.join(f"AoC{THIS_YEAR}", folder).replace(os.path.sep, "."))
                tmp = getattr(tmp, folder)
                _ = tmp()
            except (ImportError, AttributeError):
                pass


__import_days()
