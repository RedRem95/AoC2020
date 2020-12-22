from copy import deepcopy
from typing import Iterable, Tuple, List


class Combat:

    def __init__(self, *decks: Iterable[int]):
        if len(decks) < 2:
            raise Exception(f"There have to be at least 2 player to play {self.game_name()}")
        self._player_original = tuple(list(x) for x in decks)
        self._rounds = 0

    def _who_won(self, played_cards: Tuple[int, ...], current_decks: Tuple[List[int], ...]) -> List[int]:
        return [i for i, x in sorted(enumerate(played_cards), key=lambda x: x[1], reverse=True)]

    @classmethod
    def game_name(cls) -> str:
        return cls.__name__

    def get_rounds_played_last_time(self):
        return self._rounds

    def play(self, recursion_safe: bool = True) -> Tuple[int, int]:
        players = deepcopy(self._player_original)
        round_vault: Tuple[List[List[int]], ...] = tuple([[]] * len(players))
        winner = -len(players) - 1
        self._rounds = 0
        while winner < 0:
            self._rounds += 1

            playable_players = []
            for i in range(len(players)):
                if len(players[i]) > 0:
                    playable_players.append(i)

            if recursion_safe:
                one_false = False
                for i, player in ((i, players[i]) for i in playable_players):
                    if player not in round_vault[i]:
                        one_false = True
                if not one_false:
                    winner = 0
                    break

                for i, player in ((i, players[i]) for i in playable_players):
                    round_vault[i].append(deepcopy(player))

            played_cards = tuple(players[x].pop(0) for x in playable_players)
            winning_order = self._who_won(played_cards=played_cards,
                                          current_decks=tuple([players[x] for x in playable_players]))
            round_winner = players[playable_players[winning_order[0]]]
            for i in winning_order:
                round_winner.append(played_cards[i])

            if sum(1 if len(x) > 0 else 0 for x in players) == 1:
                winner = playable_players[winning_order[0]]

        return winner, sum((x + 1) * y for x, y in enumerate(reversed(players[int(winner)])))


class RecursiveCombat(Combat):

    def __init__(self, *decks: Iterable[int]):
        if len(decks) != 2:
            raise Exception(f"You can play {self.game_name()} with 2 players only. You want to play as {len(decks)}. "
                            f"I suggest you play {Combat.game_name()} instead")
        super().__init__(*decks)
        self._sub_games = 0
        self._sub_rounds = 0

    @classmethod
    def game_name(cls) -> str:
        return "Recursive Combat"

    def get_sub_games(self):
        return self._sub_games

    def get_sub_game_rounds(self):
        return self._sub_rounds

    def _who_won(self, played_cards: Tuple[int, ...], current_decks: Tuple[List[int], ...]) -> List[int]:
        if all(len(current_decks[i]) >= played_cards[i] for i in range(max(len(played_cards), len(current_decks)))):
            sub_decks = tuple(current_decks[i][:played_cards[i]] for i in range(len(current_decks)))
            sub_game = RecursiveCombat(*sub_decks)
            winner, _ = sub_game.play()
            self._sub_games += 1 + sub_game.get_sub_games()
            self._sub_rounds += sub_game.get_sub_game_rounds() + sub_game.get_rounds_played_last_time()
            return [winner] + [x for x in range(len(played_cards)) if x != winner]
        return super()._who_won(played_cards, current_decks)
