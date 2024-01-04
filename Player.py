import random

from Domino import Domino
from Enum import PlayResult
from PlayerAction import PlayerAction

class Player:
    def __init__(self, name, is_real=True, color="blue"):
        self.name = name
        self.hand: list[Domino] = []
        self.history: list[str] = []
        self.is_real = is_real
        self.color = color

    def __repr__(self) -> str:
        return self.name
    
    # def play(self, table) -> PlayResult:
    #     result = random.randint(0, 30)
    #     if result == 0 or len(self.hand) == 0:
    #         self.log(table, "OUT", f"went out!")
    #         return PlayResult.OUT
    #     else:
    #         domino = self.hand.pop(0)
    #         self.log(table, "PLACED", f"played {domino}")
    #         return PlayResult.NEXT

    def player_has_spinner(self, table):
        hand_table = self.hash_hand(table)
        for domino in hand_table[table.round]:
            if domino == table.spinner:
                domino_index = self.hand.index(domino)
                self.hand.pop(domino_index)
                
                return True
        return False

    def hash_hand(self, table):
        hand_table = {x: [] for x in range(0, table.domino_double + 1)}
        for domino in self.hand:
            hand_table[domino.left].append(domino)
            hand_table[domino.right].append(domino)

        return hand_table

    def score(self):
        score = 0
        for domino in self.hand:
            score += domino.score()
        return score

    def log(self, table, group: str, message: str):
        table.log(self, group, message)
        self.history.append(f"[{group}]: {message}")

    def add_to_hand(self, dominoes: list[Domino]):
        self.hand += dominoes
        # rehash hand
        # set has_spinner

    def remove_domino_from_hand(self, domino: Domino):
        domino_index = self.hand.index(domino)
        self.hand.pop(domino_index)

class LegalPlayer(Player):

    def play(self, table, available_trains) -> PlayerAction:
        hand_table = self.hash_hand(table)
        for train in available_trains:
            if len(hand_table[train.tip]) > 0:
                domino = hand_table[train.tip][0]
                return PlayerAction(PlayResult.PLAY, domino, train)
        return PlayerAction(PlayResult.NOPLAY)

        # if self._play_on_first_train(table, available_trains):
        #     return self._can_play(table)
        # else:
        #     self.log(table, "DRAW", f"cannot play, drawing...")
        #     if self.draw(table) == []: #no dominoes to draw
        #         self.log(table, "PASS", f"nothing to draw :(")
        #         return self._cannot_play(table)
        #     if self._play_on_first_train(table, available_trains):
        #         return self._can_play(table)
        #     else:
        #         self.log(table, "PASS", f"still cannot play")
        #         return self._cannot_play(table)

    # def _can_play(self, table) -> PlayResult:
    #     if len(self.hand) == 0:
    #         self.log(table, "OUT", f"went out!")
    #         return PlayResult.OUT
    #     return PlayResult.NEXT
    
    # def _cannot_play(self, table) -> PlayResult:
    #     self.log(table, "PASS", f"cannot play, putting penny up")
    #     table.trains[self].set_public(True)
    #     return PlayResult.PASS
    
    
                
            
        



