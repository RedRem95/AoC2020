from typing import Tuple, List

from AoC.Day import Day, StarTask
from AoC2020.Day18.Math import Formula, Operators


class Day18(Day):
    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        return [x.strip() for x in str(raw_input, "utf-8").strip().split("\n") if len(x) > 0]

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task is not None:
            return self._run(data=self.get_input(task=task), order=self.get_day_config().get(task.name, None))
        return "", None

    def _run(self, data: List[str], order: List[str]) -> Tuple[str, object]:
        formulas = [Formula(x) for x in data]
        log = [f"Going to calculate {len(formulas)} formulas"]
        if order is not None:
            log.append(f"Order of operators is: {', '.join(str(x) for x in order)}")
        else:
            log.append("No operator order given. Calculating from left to right only")
        r = sum(f.calculate(order=order) for f in formulas)
        log.append(f"Sum of all results is {r}")
        return "\n".join(str(x) for x in log), r
