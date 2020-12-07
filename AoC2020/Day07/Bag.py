from typing import Tuple, Union, Optional, List, Set, Dict, Iterable


class BagRule:
    def __init__(self, color: str, bag_rules: Dict[str, "BagRule"], can_contain: Iterable[Tuple[str, int]]):
        super(BagRule, self).__init__()
        if color is None or color in bag_rules:
            raise KeyError(f"There is already a rule for color {color}")
        self._can_contain: Dict[str, int] = dict(can_contain)
        self._color = color
        bag_rules[color] = self

    def __str__(self):
        return f"{__class__.__name__}<{self._color}->{', '.join(f'{x}[{y}]' for x, y in self._can_contain.items())}>"

    def can_contain(self, color: Union[str, "BagRule"],
                    bag_rules: Dict[str, "BagRule"],
                    search_depth: Optional[int] = None,
                    already_traveled: Set["BagRule"] = None,
                    log: List[str] = None) -> bool:
        if search_depth is not None and search_depth <= 0:
            return False
        if isinstance(color, BagRule):
            color = color._color
        if color in self._can_contain:
            return True
        if already_traveled is None:
            already_traveled = set()
        if self in already_traveled:
            if log is not None:
                log.append(f"{self} has already been traveled. Going to not search it again")
            return False
        already_traveled.add(self)
        for bag_rule, _ in self._can_contain.items():
            sub_rule = bag_rules.get(bag_rule, None)
            if sub_rule is None:
                continue
            if sub_rule.can_contain(color=color, already_traveled=already_traveled, log=log, bag_rules=bag_rules,
                                    search_depth=None if search_depth is None else search_depth - 1):
                return True
        return False

    def amount_bags_this_creates(self, bag_rules: Dict[str, "BagRule"]) -> int:
        ret = 1
        for bag_rule, amount in ((bag_rules.get(x, None), y) for x, y in self._can_contain.items()):
            if bag_rule is None:
                continue
            sub_amount = bag_rule.amount_bags_this_creates(bag_rules=bag_rules)
            ret += amount * sub_amount
        return ret
        # return sum(a * b.amount_sub_bags() for b, a in _ if b is not None)
