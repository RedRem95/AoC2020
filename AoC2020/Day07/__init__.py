from typing import Tuple, Dict

from AoC.Day import Day, StarTask
from AoC2020.Day07 import Bag


class Day07(Day):
    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        ret = {}
        for line in [x for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]:
            self._process_line(line=line, rule_collection=ret)
        return ret

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(task=StarTask.Task01)
        if task == StarTask.Task02:
            return self._run02(task=StarTask.Task01)
        return "", None

    @staticmethod
    def _process_line(line: str, rule_collection: Dict[str, Bag.BagRule]):
        def _sanitize_color(_color: str):
            return " ".join(_color.split(" ")[:-1])

        try:
            line = line.split("contain")
            own_color = _sanitize_color(line[0].strip())
            other_colors = [_sanitize_color(x.strip()).split(" ") for x in "contain".join(line[1:]).split(",")]
            try:
                other_colors = [(" ".join(x[1:]), int(x[0])) for x in other_colors]
            except ValueError:
                other_colors = []
            _ = Bag.BagRule(color=own_color, bag_rules=rule_collection, can_contain=other_colors)
        finally:
            pass

    def _run01(self, task: StarTask) -> Tuple[str, object]:
        log = []
        own_color = self.get_day_config()["own_color"]
        data = self.get_input(task=task)
        all_rules = [x for x in data.values()]
        log.append(f"Searching for '{own_color}' in {len(all_rules)} rules")
        result = sum(1 if x.can_contain(color=own_color, bag_rules=data) else 0 for x in all_rules)
        log.append(f"{result} bag colors can eventually contain a shiny gold bag")
        return "\n".join(str(x) for x in log), result

    def _run02(self, task: StarTask) -> Tuple[str, object]:
        log = []
        data = self.get_input(task=task)
        own_color = self.get_day_config()["own_color"]
        log.append(f"Checking how many bags have to go into a '{own_color}' one")
        result = data[own_color].amount_bags_this_creates(bag_rules=data)
        log.append(f"A {own_color} bag has to contain {result - 1} other bags")
        log.append(f"You will carry around {result} bags{'' if result <= 3 else '. Lol'}")
        return "\n".join(str(x) for x in log), result - 1

    def get__file__(self) -> str:
        return __file__
