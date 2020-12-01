import datetime
import json
import os
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict, List, Generator, Any, Tuple
from AoC import THIS_YEAR


def _download_input(day: int, year: int = datetime.datetime.now().year) -> Optional[str]:
    return None


__aoc_session_env = "AOC_SESSION_ID"
try:
    import requests
    SESSION_ID = os.environ.get(__aoc_session_env)
    if SESSION_ID is None:
        del SESSION_ID
        raise KeyError()

    def _download_input(day: int, year: int = None) -> Optional[str]:
        if year is None:
            year = THIS_YEAR
        cookies = {'session': SESSION_ID}
        headers = {'User-Agent': 'Mozilla/5.0'}
        print(f"Download for AOC{year}-{day}")
        response = requests.get(f'https://adventofcode.com/{year}/day/{day}/input', cookies=cookies, headers=headers)
        return response.text
except ImportError as e:
    print("Requests not installed. You wont be able to automatically download your inputs")
except KeyError as e:
    print(f"Requests installed. But you need to set the \"{__aoc_session_env}\" environment variable")


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
        config_content = self.get_file_content_raw("config.json")
        if config_content is not None:
            self.__config = json.loads(config_content)

    def get_input(self, task: StarTask):
        return self.__day_input.get(task, None)

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

        for i, middle_part in enumerate([self.get_name(),
                                         f"{self.get_name()}: {str(datetime.timedelta(seconds=sum(durations.values())))}"
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
        for day in sorted(cls.__loaded_days, key=lambda x: x.get_name()):
            yield day

    def get_file_content_raw(self, file_name: str) -> Optional[bytes]:
        file_name = os.path.join(os.path.dirname(self.get__file__()), file_name)
        if not os.path.exists(file_name):
            return None
        with open(file_name, "rb") as fin:
            return fin.read()

    def get_input_content_raw(self, task: StarTask) -> Optional[bytes]:
        data = self.get_file_content_raw(f"input_{task.value}.txt")
        if task == StarTask.Task01 and data is None:
            day = self.get_day()
            if day is not None:
                downloaded_data = _download_input(day)
                if downloaded_data is not None:
                    downloaded_data = downloaded_data.encode("utf-8")
                    with open(os.path.join(os.path.dirname(self.get__file__()), f"input_{task.value}.txt"), "wb") \
                            as fout:
                        fout.write(downloaded_data)
                    return downloaded_data
        return data

    def get_name(self) -> str:
        return self.__class__.__name__

    def get_day(self) -> Optional[int]:
        try:
            return int(self.get_name()[3:])
        except (ValueError, KeyError):
            return None
