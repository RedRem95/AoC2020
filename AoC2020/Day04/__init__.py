from typing import Tuple, Dict, Callable

from AoC.Day import Day, StarTask
from AoC2020.Day04.PassportValidators import VALIDATORS_REQUIRED, VALIDATORS_OPTIONAL, KEYS


class Day04(Day):

    def __init__(self):
        super().__init__()

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        data = []
        curr_passport = {}
        for line in [x for x in str(raw_input, "utf-8").split("\n")]:
            if len(line) <= 0:
                if len(curr_passport) > 0:
                    data.append(curr_passport)
                curr_passport = {}
                continue
            line_data = line.split(" ")
            for data_split in line_data:
                curr_passport[data_split.split(":")[0]] = ":".join(data_split.split(":")[1:])
        if len(curr_passport) > 0:
            data.append(curr_passport)
        return data

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run(task=task,
                             validator_required=dict((x, lambda y: True) for x in VALIDATORS_REQUIRED.keys()),
                             validator_optional=dict((x, lambda y: True) for x in VALIDATORS_OPTIONAL.keys()))
        if task == StarTask.Task02:
            return self._run(task=task,
                             validator_required=VALIDATORS_REQUIRED,
                             validator_optional=VALIDATORS_OPTIONAL)
        return "", None

    def _run(self,
             validator_required: Dict[str, Callable[[str], bool]],
             validator_optional: Dict[str, Callable[[str], bool]],
             task: StarTask = StarTask.Task01) -> Tuple[str, object]:
        log = []
        result = 0
        data = self.get_input(task=task)
        log.append(f"Checking {len(data)} passports "
                   f"with {len(validator_required)} required and {len(validator_optional)} optional fields")
        for data_line in data:
            if self._validate_passport(passport=data_line,
                                       validator_required=validator_required,
                                       validator_optional=validator_optional):
                result += 1
        log.append(f"{(result / len(data)) * 100:6.2f}% [{result}/{len(data)}] passports are valid")
        return "\n".join(str(x) for x in log), result

    @staticmethod
    def _validate_passport(passport: Dict[str, str],
                           validator_required: Dict[str, Callable[[str], bool]],
                           validator_optional: Dict[str, Callable[[str], bool]]) -> bool:
        return all(key in passport and validator(passport[key]) for key, validator in validator_required.items())

    def get__file__(self) -> str:
        return __file__
