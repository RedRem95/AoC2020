from typing import Tuple, List

from AoC.Day import Day, StarTask
from AoC2020.Day19.Ruling import RuleSet


class Day19(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        ret = [[]]
        for x in [x.strip() for x in str(raw_input, "utf-8").strip().split("\n")]:
            if len(x) <= 0:
                ret.append([])
            else:
                ret[-1].append(x)
        return tuple(ret[:2])

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task is not None:
            return self._run(data=self.get_input(task=task), replacements=self.get_day_config().get(task.name, None))
        return "", None

    @staticmethod
    def _run(data: Tuple[List[str], List[str]], replacements: List[str] = None) -> Tuple[str, object]:
        if replacements is None:
            replacements = []

        rule_set = RuleSet(rule_lines=data[0])
        count1 = rule_set.count_rules()
        rule_set.set_ruling(replacements)
        count2 = rule_set.count_rules()
        r = sum(1 if rule_set.match_text(text=x, index=0, match_whole=True) else 0 for x in data[1])

        log = [
            f"Loaded ruleset with {count2} rules",
            f"Added {count2 - count1} rules",
            f"Replaced {len(replacements) - (count2 - count1)} rules",
            f"Validated {len(data[1])} lines",
            f"{(r / len(data[1])) * 100:6.2f}% [{r}/{len(data[1])}] lines are valid"
        ]

        return "\n".join(str(x) for x in log), r
