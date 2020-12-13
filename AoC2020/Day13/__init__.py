from typing import Tuple, Dict

from AoC.Day import Day, StarTask


class Day13(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        raw_data = [x for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]

        def _to_int(v: str):
            try:
                return int(v)
            except ValueError:
                pass
            return None

        return {"your_time": int(raw_data[0]),
                "busses": [_to_int(y.strip()) for y in raw_data[1].split(",")]}

    def get__file__(self) -> str:
        return __file__

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(data=self.get_input(task=StarTask.Task01))
        if task == StarTask.Task02:
            return self._run02(data=self.get_input(task=StarTask.Task01))
        return "", None

    def _run01(self, data: Dict) -> Tuple[str, object]:
        log = []
        your_time = data["your_time"]
        busses = sorted(x for x in data["busses"] if x is not None)
        log.append(f"You arrive at {your_time}")
        log.append(f"Busses in service {len(busses)} [{', '.join(str(x) for x in busses)}]")
        best_bus, wait_time = sorted([(x, x - (your_time % x)) for x in busses], key=lambda x: x[1])[0]
        log.append(f"Best bus you can take is {best_bus}. It leaves in {wait_time} at {your_time + wait_time}")
        return "\n".join(str(x) for x in log), best_bus * wait_time

    def _run02(self, data: Dict) -> Tuple[str, object]:
        log = []
        busses = dict((x, y) for x, y in enumerate(data["busses"]) if y is not None)
        log.append(f"Busses in service {len(busses)} [{', '.join(str(busses[x]) for x in sorted(busses.keys()))}]")
        current = busses[0]
        current_step_size = busses[0]
        for i in sorted(busses.keys())[1:]:
            log.append(f"Bus<{busses[i]:3d}> should arrive {i:2d} minutes after Bus<{busses[0]}>")
            while (current + i) % busses[i] != 0:
                current += current_step_size

            current_step_size *= busses[i]

        log.append(f"Found timestamp {current} where all {len(busses)} rules are true")
        return "\n".join(str(x) for x in log), current
