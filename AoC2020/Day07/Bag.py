from typing import Tuple, Union, Optional, List, Set, Dict, Generator

_bag_rules: Dict[str, "BagRule"] = {}


class BagRule:
    def __init__(self, color: str, *can_contain: Tuple[str, int]):
        super(BagRule, self).__init__()
        if color is None or color in _bag_rules:
            raise KeyError(f"There is already a rule for color {color}")
        self._can_contain: Dict[str, int] = dict(can_contain)
        self._color = color
        _bag_rules[color] = self

    def __str__(self):
        return f"{__class__.__name__}<{self._color}->{', '.join(f'{x}[{y}]' for x, y in self._can_contain.items())}>"

    def can_contain(self, color: Union[str, "BagRule"],
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
            sub_rule = get_bag_by_color(bag_rule)
            if sub_rule is None:
                continue
            if sub_rule.can_contain(color=color, already_traveled=already_traveled, log=log,
                                    search_depth=None if search_depth is None else search_depth - 1):
                return True
        return False

    def amount_bags_this_creates(self) -> int:
        ret = 1
        for bag_rule, amount in ((get_bag_by_color(x), y) for x, y in self._can_contain.items()):
            if bag_rule is None:
                continue
            sub_amount = bag_rule.amount_bags_this_creates()
            ret += amount * sub_amount
        return ret
        # return sum(a * b.amount_sub_bags() for b, a in _ if b is not None)


def get_bag_by_color(color: str) -> BagRule:
    return _bag_rules.get(color, None)


def iterate_rules() -> Generator[BagRule, BagRule, None]:
    for _bag_rule in _bag_rules.values():
        yield _bag_rule
