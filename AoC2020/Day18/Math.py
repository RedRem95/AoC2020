from typing import Union, List, Callable, Dict, Tuple


class Operators:
    _all_operators: Dict[str, "Operators"] = {}

    def __init__(self, symbol: str, calculation: Callable[[float, float], float]):
        self._symbol = symbol
        self._calculation = calculation
        self.__class__._all_operators[symbol] = self

    def get_symbol(self) -> str:
        return self._symbol

    def calculate(self, x: float, y: float) -> float:
        return self._calculation(x, y)

    @classmethod
    def get_operator(cls, symbol: str) -> "Operators":
        return cls._all_operators.get(symbol, None)

    def __str__(self):
        return self.get_symbol()

    def __repr__(self):
        return f"{self.get_symbol()} Operator"


Operators(symbol="*", calculation=lambda x, y: x * y)
Operators(symbol="+", calculation=lambda x, y: x + y)


class Formula:

    def __init__(self, line: str):
        self._values: List[Union[float, "Formula"]] = []
        self._operators: List[Operators] = []
        line = [x for x in line.split(" ") if len(x) > 0]
        i = 0
        while i < len(line):
            if len(self._values) > len(self._operators):
                current_operator = Operators.get_operator(line[i])
                if current_operator is None:
                    raise KeyError(f"{line[i]} is no valid Operator")
                self._operators.append(current_operator)
            else:
                if line[i].startswith("("):
                    j = i
                    open_parenthesis = 0
                    while j < len(line):

                        for el in line[j]:
                            if el == "(":
                                open_parenthesis += 1
                            if el == ")":
                                open_parenthesis -= 1
                        if open_parenthesis <= 0:
                            self._values.append(Formula(" ".join(line[i:j + 1])[1:-1]))
                            break
                        j += 1
                    i = j
                else:
                    self._values.append(float(line[i]))
            i += 1

    @staticmethod
    def _get_value_at(values: List[Union["Formula", float]], index: int, order: List[str]) -> float:
        return values[index].calculate(order=order) if isinstance(values[index], Formula) else values[index]

    def calculate(self, order: List[str] = None) -> float:
        order = [] if order is None else order
        values = [x for x in self._values]
        operators = [x for x in self._operators]
        _inf = float("inf")

        def key(x: Tuple[int, Operators]):
            return order.index(x[1].get_symbol()) if x[1].get_symbol() in order else _inf

        def next_operator() -> Tuple[int, Operators]:
            return sorted(((_i, _op) for _i, _op in enumerate(operators)), reverse=False, key=key)[0]

        i = 0
        while len(operators) > 0:
            i, op = next_operator()
            v1 = self._get_value_at(values=values, index=i, order=order)
            v2 = self._get_value_at(values=values, index=i + 1, order=order)
            v = op.calculate(x=v1, y=v2)
            values[i] = v
            del values[i + 1]
            del operators[i]

        return values[i].calculate(order=order) if isinstance(values[i], Formula) else values[i]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        current = []
        try:
            if isinstance(self._values[0], Formula):
                current.append(f"({str(self._values[0])})")
            else:
                current.append(str(self._values[0]))
        except IndexError:
            return 0

        for i, op in enumerate(self._operators):
            current.append(op.get_symbol())
            if isinstance(self._values[i + 1], Formula):
                current.append(f"({str(self._values[i + 1])})")
            else:
                current.append(str(self._values[i + 1]))

        return " ".join(current)
