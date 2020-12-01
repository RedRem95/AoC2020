import datetime
import json
import os
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict, List, Generator, Any, Tuple


class StarTask(Enum):
    Task01 = 1
    Task02 = 2


class Day(ABC):
    __loaded_days: List["Day"] = []

    def __init__(self):
        self.__day_input: Dict[StarTask, object] = {}
        for task in StarTask:
            data = self.get_input_content_raw(task=task)
            if data is not None:
                self.__day_input[task] = self.convert_input(raw_input=data, task=task)
        self.__class__.__loaded_days.append(self)
        self.__config: Dict[str, object] = {}
        config_file = os.path.join(os.path.dirname(self.get__file__()), "config.json")
        if os.path.exists(config_file):
            with open(config_file, "rb") as fin:
                self.__config = json.load(fin)

    def get_input(self, task: StarTask):
        return self.__day_input[task]

    def get_day_config(self) -> Dict[str, Any]:
        return self.__config

    @abstractmethod
    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        pass

    @abstractmethod
    def run(self, task: StarTask) -> Tuple[str, object]:
        pass

    @abstractmethod
    def get__file__(self) -> str:
        return __file__

    def run_all(self, show_log: bool = True) -> Tuple[str, Dict[StarTask, object], Dict[StarTask, float]]:
        res = []
        all_max = 15 + 5
        results = {}
        durations = {}
        for task in sorted(StarTask, key=lambda x: x.value):
            res.append(f"{task.name:6}:")
            start_time = time.time()
            log, result = self.run(task=task)
            end_time = time.time()
            duration = end_time - start_time
            results[task] = result
            durations[task] = duration
            if result is None:
                res.append("<<Not done>>")
                continue
            if show_log:
                log = log.split("\n")
            else:
                log = []
            result: str = f"Copy me: '{result}'"
            time_str: str = f"   Time: '{datetime.timedelta(seconds=duration)}'"
            max_len = max([len(x) for x in log] + [1, len(result), len(time_str)])
            template = "|{line:%s}|" % max_len
            if show_log:
                res.append(f"|log:{'=' * (max_len - 4)}|")
                for line in log:
                    res.append(template.format(line=line))
                res.append(f"|result:{'-' * (max_len - 7)}|")
            else:
                res.append(f"|result:{'=' * (max_len - 7)}|")
            res.append(template.format(line=result))
            res.append(template.format(line=time_str))
            res.append(f"|{'=' * max_len}|")
            all_max = max(all_max, max_len + 2)

        for i, middle_part in enumerate([self.__class__.__name__,
                                         f"{self.__class__.__name__}: {str(datetime.timedelta(seconds=sum(durations.values())))}"
                                         ]):
            first_part = "~" * int((all_max - len(middle_part)) / 2)
            back_part = "~" * int(all_max - len(first_part) - len(middle_part))
            middle_part = "".join([first_part, middle_part, back_part])
            if i == 0:
                res.insert(0, middle_part)
            else:
                res.append(middle_part)

        return "\n".join(res), results, durations

    @classmethod
    def iterate_days(cls) -> Generator["Day", "Day", None]:
        for day in sorted(cls.__loaded_days, key=lambda x: x.__class__.__name__):
            yield day

    def get_input_content_raw(self, task: StarTask) -> Optional[bytes]:
        file_name = os.path.join(os.path.dirname(self.get__file__()), f"input_{task.value}.txt")
        if not os.path.exists(file_name):
            return None
        with open(file_name, "rb") as fin:
            return fin.read()


def __import_days():
    import re
    import importlib
    pattern = re.compile(r"Day[0-2][0-9]")
    parent_parent = os.path.dirname(os.path.dirname(__file__))
    for folder in (x for x in os.listdir(parent_parent) if pattern.match(x)):
        folder_abs = os.path.join(parent_parent, folder)
        if os.path.exists(folder_abs) and os.path.isdir(folder_abs) and os.path.exists(
                os.path.join(folder_abs, "__init__.py")):
            tmp = importlib.import_module(folder.replace(os.path.sep, "."))
            tmp = getattr(tmp, folder)
            _ = tmp()


__import_days()
