from typing import Tuple, List, Type, Dict

from AoC.Day import Day, StarTask
from AoC2020.Day22.Gaming import Combat, RecursiveCombat


class Day22(Day):
    _task_games: Dict[StarTask, Type[Combat]] = {
        StarTask.Task01: Combat,
        StarTask.Task02: RecursiveCombat
    }

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        p2_cards = []
        p1_cards = []
        p1 = True
        for line in [x.strip() for x in str(raw_input, "utf-8").strip().split("\n")]:
            if len(line) <= 0:
                if not p1:
                    break
                p1 = False
                continue
            try:
                if p1:
                    p1_cards.append(int(line))
                else:
                    p2_cards.append(int(line))
            except ValueError:
                pass
        return p1_cards, p2_cards

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task in self.__class__._task_games:
            return self._run(data=self.get_input(task=task), game_type=self.__class__._task_games[task])
        return "", None

    @staticmethod
    def _run(data: Tuple[List[int], List[int]], game_type: Type[Combat] = Combat) -> Tuple[str, object]:
        game = game_type(*data)
        winner, score = game.play(recursion_safe=True)
        log = [
            f"Game played: {game.game_name()}",
            f"Winner:      {winner + 1}",
            f"Game Rounds: {game.get_rounds_played_last_time()}",
            f"Score:       {score}"
        ]
        if isinstance(game, RecursiveCombat):
            log.append(f"Sub games:   {game.get_sub_games()}")
            log.append(f"Sub rounds:  {game.get_sub_game_rounds()}")
            log.append(f"All rounds:  {game.get_sub_game_rounds() + game.get_rounds_played_last_time()}")
        return "\n".join(str(x) for x in log), score
