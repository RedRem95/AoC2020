from typing import Tuple, List, Dict

from AoC.Day import Day, StarTask


class Day10(Day):
    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        ret = []
        for line in [x for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]:
            ret.append(int(line))
        return ret

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(data=self.get_input(task=StarTask.Task01))
        if task == StarTask.Task02:
            return self._run02(data=self.get_input(task=StarTask.Task01))
        return "", None

    def _run01(self, data: List[int]) -> Tuple[str, object]:
        log = []
        differences = self._measure_differences(data=data, log=log)
        return "\n".join(str(x) for x in log), differences.get(1, 0) * differences.get(3, 0)

    def _run02(self, data: List[int]):
        log = []
        count_good_arrangements = self._count_arrangements(data=data, log=log)
        return "\n".join(str(x) for x in log), count_good_arrangements

    @staticmethod
    def _measure_differences(data: List[int], fixed_end: int = None, fixed_start: int = 0,
                             possible_diff: Tuple[int, int] = (1, 3), log: List[str] = None) -> Dict[int, int]:
        if log is not None:
            log.append(f"Going to count step-sizes in your {len(data)} adapters")
        data = sorted(list(data) + [fixed_start, max(data) + max(possible_diff) if fixed_end is None else fixed_end])
        differences: Dict[int, int] = {}
        for i in range(1, len(data)):
            diff = data[i] - data[i - 1]
            if min(possible_diff) <= diff <= max(possible_diff):
                differences[diff] = differences.get(diff, 0) + 1
        if log is not None:
            for step_size in range(min(possible_diff), max(possible_diff) + 1, 1):
                log.append(f"Your adapters make {differences.get(step_size, 0)} times a step of size {step_size}")
        return differences

    @staticmethod
    def _count_arrangements(data: List[int], fixed_end: int = None, fixed_start: int = 0,
                            possible_diff: Tuple[int, int] = (1, 3), log: List[str] = None) -> int:
        collection: Dict[int, int] = {fixed_start: 1}
        fixed_end = max(data) + max(possible_diff) if fixed_end is None else fixed_end
        if log is not None:
            log.append(f"Going to check in how many ways you can arrange your {len(data)} adapters")
            log.append(f"You want to get from {fixed_start} to {fixed_end} yolts")
        for current in sorted(list(data) + [fixed_end]):
            usable_count = 0
            for prev_outlet in range(current - max(possible_diff), current - min(possible_diff) + 1, 1):
                usable_count += collection.get(prev_outlet, 0)
            collection[current] = usable_count
        if log is not None:
            log.append(f"There are {collection.get(fixed_end, 0)} ways you can arrange your adapters. Have fun")
        return collection.get(fixed_end, 0)

    def get__file__(self) -> str:
        return __file__
