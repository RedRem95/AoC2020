from typing import Tuple

from AoC.Day import Day, StarTask
from AoC2020.Day08 import today_instructions as day08_instructions
from AoC2020.Day08.InstructionCode import InstructionMachine, CodeLine


class Day09(Day):
    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        ret = []
        for line in [x for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]:
            ret.append(CodeLine.parse(line))
        return ret

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(task=StarTask.Task01)
        if task == StarTask.Task02:
            return self._run02(task=StarTask.Task02)
        return "", None

    def _run01(self, task):
        log = []
        result = 0
        data = self.get_input(task=task)
        instructions = day08_instructions()
        instructions.update({})
        machine = InstructionMachine(machine_code=data, registered_instructions=instructions.values())
        machine.run()
        for data_line in data:
            result += 1

        return "\n".join(str(x) for x in log), result

    def _run02(self, task):
        log = []
        result = 0
        data = self.get_input(task=task)
        for data_line in data:
            result += 1

        return "\n".join(str(x) for x in log), result

    def get__file__(self) -> str:
        return __file__
