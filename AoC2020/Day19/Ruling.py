from abc import ABC, abstractmethod
from typing import Tuple, List, Dict, Generator


class _Rule(ABC):
    @abstractmethod
    def valid(self, text: str) -> Generator[Tuple[bool, int], Tuple[bool, int], None]:
        pass


class RuleSet:

    def __init__(self, rule_lines: List[str]) -> None:
        super().__init__()
        self._rules: Dict[int, _Rule] = {}
        self.set_ruling(rule_lines=rule_lines)

    def set_ruling(self, rule_lines: List[str]) -> "RuleSet":
        for line in rule_lines:
            line = [x.strip() for x in line.split(":")]
            ruling = line[1]
            if ruling.startswith("\""):
                self._rules[int(line[0])] = _MatchRule(match=ruling[1:-1])
            else:
                self._rules[int(line[0])] = _CallingRule(rule_set=self,
                                                         other_ids=[[int(y.strip()) for y in x.strip().split(" ")] for x
                                                                    in ruling.split("|")])
        return self

    def get_rule(self, index: int) -> _Rule:
        return self._rules[index]

    def match_text(self, text: str, index: int = 0, match_whole: bool = True):
        for res in self.get_rule(index=index).valid(text=text):
            if res[0] and ((not match_whole) or res[1] == len(text)):
                return True
        return False

    def count_rules(self):
        return len(self._rules)

    def __str__(self):
        ret = [f"Ruleset with {self.count_rules()} rules"]
        for rule in sorted(self._rules.keys()):
            ret.append(f"  => {rule}: {str(self.get_rule(rule))}")
        return "\n".join(ret)


class _MatchRule(_Rule):

    def __init__(self, match: str) -> None:
        super().__init__()
        self._match = match

    def valid(self, text: str) -> Generator[Tuple[bool, int], Tuple[bool, int], None]:
        if text.startswith(self._match):
            yield True, len(self._match)
        else:
            yield False, -1

    def get_match(self):
        return self._match

    def __str__(self):
        return f"\"{self.get_match()}\""


class _CallingRule(_Rule):

    def __init__(self, rule_set: RuleSet, other_ids: List[List[int]]) -> None:
        super().__init__()
        self._rule_set = rule_set
        self._other_ids = [x for x in other_ids]

    def valid(self, text: str) -> Generator[Tuple[bool, int], Tuple[bool, int], None]:
        if len(text) <= 0:
            yield False, -1
            return
        for other_ids in self._other_ids:
            current = [0]
            for rule in (self._rule_set.get_rule(index=x) for x in other_ids):
                current_tmp = [x for x in current]
                current = []
                for c in current_tmp:
                    for valid, steps in rule.valid(text=text[c:]):
                        if valid:
                            current.append(c + steps)
            for c in current:
                yield True, c

    def __str__(self):
        # ret = ["".join(str(x) for x in (self._rule_set.get_rule(index=y) for y in ids)) for ids in self._other_ids]
        return " | ".join(" ".join(str(y) for y in x) for x in self._other_ids)
