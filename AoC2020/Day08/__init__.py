from typing import Tuple, List, Union

from AoC.Day import Day, StarTask
from AoC2020.Day08.InstructionCode import InstructionMachine, CodeLine, JMP, ACC, NOP, Instruction, ExitCodes


def today_instructions():
    return dict((x.instruction_key(), x) for x in [JMP(), NOP(), ACC()])


class Day08(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        return [x for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(task=StarTask.Task01)
        if task == StarTask.Task02:
            return self._run02(task=StarTask.Task01)
        return "", None

    def _run(self, data: List[Union[str, CodeLine]] = None) -> Tuple[List[str], int, ExitCodes]:
        log = []
        if data is None:
            data = self.get_input(task=StarTask.Task01)
        data = [x if isinstance(x, CodeLine) else CodeLine.parse(x) for x in data]
        instructions = today_instructions()
        log.append(f"Executing machine on {len(data)} lines of code")
        log.append(f"Executing machine with {len(instructions)} instructions: {', '.join(sorted(instructions.keys()))}")
        machine = InstructionMachine(machine_code=data, registered_instructions=instructions.values())
        exit_code = machine.run()
        ret = int(instructions["acc"].get_value())
        log.append(f"Machine exited with code: {exit_code.value} ({exit_code.name})")
        log.append(f"Accumulator produced value: {ret}")
        return log, ret, exit_code

    def _run01(self, task: StarTask = StarTask.Task01) -> Tuple[str, object]:
        ret = self._run(data=self.get_input(task=task))
        return "\n".join(str(x) for x in ret[0]), ret[1]

    def _run02(self, task: StarTask = StarTask.Task01, swap: Tuple[str, str] = ("jmp", "nop")) -> Tuple[str, object]:
        raw_data = [CodeLine.parse(x) for x in self.get_input(task=task)]
        for i, code_line in enumerate(raw_data):
            use_data = None
            log = []
            if code_line.get_instruction() == swap[0]:
                use_data = [x if j != i else CodeLine(swap[1], code_line.get_value()) for j, x in enumerate(raw_data)]
                log = [f"Had to swap in line {i + 1}: {swap[0]} -> {swap[1]}"]
            if code_line.get_instruction() == swap[1]:
                use_data = [x if j != i else CodeLine(swap[0], code_line.get_value()) for j, x in enumerate(raw_data)]
                log = [f"Had to swap in line {i + 1}: {swap[1]} -> {swap[0]}"]
            if use_data is not None:
                res = self._run(data=use_data)
                if res[2] == ExitCodes.Good:
                    log = res[0] + log
                    return "\n".join(str(x) for x in log), res[1]
        return "", None

    def get__file__(self) -> str:
        return __file__
