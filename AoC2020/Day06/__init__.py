from typing import Tuple

import AoC.misc
from AoC.Day import Day, StarTask


class Day06(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        ret = []
        for line in [x for x in str(raw_input, "utf-8").split("\n")]:
            ret.append(line)
        return ret

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(StarTask.Task01)
        if task == StarTask.Task02:
            return self._run02(StarTask.Task01)
        return "", None

    @staticmethod
    def _process_answers(data):
        ret = [[]]
        for data_line in data:
            if len(data_line) <= 0:
                ret.append([])
                continue
            ret[-1].append([x for x in data_line if x != " "])
        return [x for x in ret if len(x) > 0]

    def _run01(self, task: StarTask) -> Tuple[str, object]:
        log = []
        data = self.get_input(task=task)
        log.append(f"Processing {len(data)} lines of data")
        answers = self._process_answers(data=data)
        log.append(f"Checking answers of {len(answers)} groups")
        log.append(f"Checking answers of {sum(len(group) for group in answers)} persons")
        result = sum(len(set(sum(group, []))) for group in answers)
        log.append(f"The sum of the count of all at least once given answers in each group is {result}. "
                   f"No use in knowing that")
        log.append(f"Each group had {result / len(answers):.2f} different answers on average")
        log.append(f"Each group had {sum(len(group) for group in answers) / len(answers):.2f} persons on average")
        return "\n".join(log), result

    def _run02(self, task: StarTask) -> Tuple[str, object]:
        log = []
        data = self.get_input(task=task)
        log.append(f"Processing {len(data)} lines of data")
        answers = self._process_answers(data=data)
        log.append(f"Checking answers of {len(answers)} groups")
        log.append(f"Checking answers of {sum(len(group) for group in answers)} persons")
        result = sum(len(AoC.misc.common(*[set(x) for x in group])) for group in answers)
        log.append(f"The sum of the count of unanimous answers in each group is {result}. There is no use in this info")
        log.append(f"Each group had {result / len(answers):.2f} unanimous answers on average")
        log.append(f"Each group had {sum(len(group) for group in answers) / len(answers):.2f} persons on average")
        return "\n".join(log), result

    def get__file__(self) -> str:
        return __file__
