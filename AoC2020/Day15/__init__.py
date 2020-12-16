from typing import Tuple, List

from AoC.Day import Day, StarTask


class Day15(Day):
    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        line = [x.strip() for x in str(raw_input, "utf-8").split("\n") if len(x.strip()) > 0][0]
        return [int(x) for x in line.split(",")]

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run(task=task)
        if task == StarTask.Task02:
            return self._run(task=task)
        return "", None

    def _run(self, task: StarTask):
        data: List[int] = self.get_input(task=task)
        target = int(self.get_day_config()[task.name])
        log = [
            f"Game starts with {len(data)} starting numbers",
            f"Starting numbers are {', '.join(str(x) for x in data)}",
            f"Searching for {target}. number in game"
        ]
        spoken_list = dict((x, [i]) for i, x in enumerate(data))
        current = len(data)
        last = data[-1]
        while current < target:
            if len(spoken_list.get(last, [])) <= 1:
                last = 0
            else:
                last = spoken_list[last][-1] - spoken_list[last][-2]
            if last not in spoken_list:
                spoken_list[last] = []
            spoken_list[last].append(current)
            current += 1
        log.append(f"The {current}. number spoken is {last}")
        log.append(f"Until now {len(spoken_list)} distinct numbers have been spoken")
        log.append(f"{max(spoken_list.keys())} has been the highest and {min(spoken_list.keys())} the lowest")
        sorted_thing = sorted(((x, len(y)) for x, y in spoken_list.items()), key=lambda x: x[1])
        log.append(f"{sorted_thing[-1][0]} has been spoken the highest amount at {sorted_thing[-1][1]} times")
        log.append(f"{sorted_thing[0][0]} has been spoken the least amount at {sorted_thing[0][1]} times")
        return "\n".join(str(x) for x in log), last
