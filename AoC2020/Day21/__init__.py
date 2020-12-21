from typing import Tuple, List, Dict, Set

from AoC.Day import Day, StarTask


class Day21(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        ingredients_in_dishes: List[Set[str]] = []
        allergens: Dict[str, List[Set[str]]] = {}
        for line in [x.strip() for x in str(raw_input, "utf-8").strip().split("\n") if len(x) > 0]:
            line_ingredients = [x.strip() for x in line.split("(")[0].split(" ") if len(x.strip()) > 0]
            line_allergens = [x.strip() for x in line.split("(contains")[1][:-1].split(",")]
            ingredients_in_dishes.append(set(line_ingredients))
            for allergen in line_allergens:
                if allergen not in allergens:
                    allergens[allergen] = []
                allergens[allergen].append(set(x for x in line_ingredients))

        return ingredients_in_dishes, allergens

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run01(data=self.get_input(task=task))
        if task == StarTask.Task02:
            return self._run02(data=self.get_input(task=task))
        return "", None

    def _run01(self, data: Tuple[List[Set[str]], Dict[str, List[Set[str]]]]) -> Tuple[str, object]:
        ingredients: Set[str] = set()
        ingredients_in_dishes: List[Set[str]] = data[0]
        allergens: Dict[str, List[Set[str]]] = data[1]

        for dish in ingredients_in_dishes:
            for ingredient in dish:
                ingredients.add(ingredient)

        ingredients_contain_nothing = set(x for x in ingredients)
        for allergen, dishes in allergens.items():
            for ingredient in dishes[0]:
                if all([ingredient in d for d in dishes[1:]] + [True]):
                    try:
                        ingredients_contain_nothing.remove(ingredient)
                    except KeyError:
                        pass

        r = 0
        for dish in ingredients_in_dishes:
            r += sum(1 if i in ingredients_contain_nothing else 0 for i in dish)

        log = [f"Checked {len(data[0])} dishes",
               f"There are {len(allergens)} allergens listed",
               f"There are {len(ingredients)} ingredients listed",
               f"There are {len(ingredients_contain_nothing)} ingredients that contain no allergen",
               f"These safe ingredients appear {r} times on the menu"]

        return "\n".join(str(x) for x in log), r

    def _run02(self, data: Tuple[List[Set[str]], Dict[str, List[Set[str]]]]) -> Tuple[str, object]:

        condensed_allergens: Dict[str, Set[str]] = dict((x, set()) for x in data[1].keys())
        for allergen, dishes in data[1].items():
            for ingredient in dishes[0]:
                if all([ingredient in d for d in dishes[1:]] + [True]):
                    condensed_allergens[allergen].add(ingredient)

        condensed_allergens: Dict[str, List[str]] = dict((x, list(y)) for x, y in condensed_allergens.items())

        counter = 0
        while any(len(ingredients) != 1 for ingredients in condensed_allergens.values()):
            counter += 1
            did_something = False
            for allergen, ingredients in condensed_allergens.items():
                if len(ingredients) < 1:
                    raise Exception(f"{allergen} seems to be in no dish")
                if len(ingredients) == 1:
                    for other_allergen in (x for x in condensed_allergens.keys() if x != allergen):
                        try:
                            condensed_allergens[other_allergen].remove(ingredients[0])
                            did_something = True
                        except ValueError:
                            pass
            if not did_something:
                raise Exception("Some allergens dont eliminate each other. Please check input")

        evil_ingredients: List[Tuple[str, str]] = sorted([(x[0], y) for y, x in condensed_allergens.items()],
                                                         key=lambda x: x[1].lower())
        canonical_dangerous_ingredient_list = ",".join(x[0] for x in evil_ingredients)

        log = [f"Checked {len(data[0])} dishes",
               f"There are {len(condensed_allergens)} allergens listed",
               f"Ingredients that contain these allergens:"]

        log.extend([f"  -> {i} contains {a}" for i, a in evil_ingredients])
        log.append(f"cdil: {canonical_dangerous_ingredient_list}")
        log.append(f"It took {counter} iterations to get this")

        return "\n".join(str(x) for x in log), canonical_dangerous_ingredient_list
