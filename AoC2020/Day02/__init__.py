from typing import Tuple, List

from AoC.Day import Day, StarTask
from AoC2020.Day02 import Validators


class Day02(Day):

    def __init__(self):
        super().__init__()

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        ret = []
        for line in [str(x) for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]:
            line = line.split(":")
            minimum = int(line[0].split("-")[0])
            maximum = int(line[0].split("-")[1].split(" ")[0])
            character = line[0].split(" ")[1]
            ret.append((minimum, maximum, character, line[1]))
        return ret

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self.__run(Validators.SledRental())
        if task == StarTask.Task02:
            return self.__run(Validators.Toboggan())
        return "Not yet done", None

    def __run(self, validator: Validators.Validator, task: StarTask = StarTask.Task01) -> Tuple[str, object]:
        data: List[Tuple[int, int, str, str]] = self.get_input(task=task)
        result = 0
        log = [f"Going to validate {len(data)} using \"{validator.get_name()}\""]
        for data_line in data:
            if validator.validate(*data_line):
                result += 1
        log.append(f"{100 * result / len(data):6.2f}% [{result}/{len(data)}] passwords are valid")
        return "\n".join(log), result

    def get__file__(self) -> str:
        return __file__
