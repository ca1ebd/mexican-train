import random

from Domino import Domino
from Enum import PlayResult

class Player:
    def __init__(self, name):
        self.name = name
        self.hand: list[Domino] = []
        self.history: list[str] = []

    def __repr__(self) -> str:
        return self.name

    def draw(self, table, num: int = 1):
        if len(table.pool) == 0:
            return []
        drawn = [table.pool.pop(random.randint(0, len(table.pool) - 1)) for x in range(0, num)]
        self.hand += drawn
        self.log(table, "DRAW", f"drew: {drawn}")
        return drawn
    
    def play(self, table) -> PlayResult:
        result = random.randint(0, 30)
        if result == 0 or len(self.hand) == 0:
            self.log(table, "OUT", f"went out!")
            return PlayResult.OUT
        else:
            domino = self.hand.pop(0)
            self.log(table, "PLACED", f"played {domino}")
            return PlayResult.NEXT
        
    def play_domino(self, table, train, domino):
        domino_index = self.hand.index(domino)
        train.add_domino(self.hand.pop(domino_index))
        if train == table.trains[self]:
            train.set_public(False)


    def draw_hand(self, table, players_draw_num):
        self.hand = []
        self.draw(table, players_draw_num)
    
    def player_has_spinner(self, table):
        hand_table = self.hash_hand(table)
        for domino in hand_table[table.round]:
            if domino == table.spinner:
                domino_index = self.hand.index(domino)
                self.hand.pop(domino_index)
                self.log(table, "SPINNER", f"I have the spinner: {domino}")
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

class LegalPlayer(Player):
    def _play_on_first_train(self, table, trains):
        hand_table = self.hash_hand(table)
        for train in trains:
            if len(hand_table[train.tip]) > 0:
                domino = hand_table[train.tip][0]
                self.play_domino(table, train, domino)
                self.log(table, "PLACED", f"played {domino} on {train}")
                return True
        return False

    def _can_play(self, table) -> PlayResult:
        if len(self.hand) == 0:
            self.log(table, "OUT", f"went out!")
            return PlayResult.OUT
        return PlayResult.NEXT
    
    def _cannot_play(self, table) -> PlayResult:
        self.log(table, "PASS", f"cannot play, putting penny up")
        table.trains[self].set_public(True)
        return PlayResult.PASS
    
    def play(self, table) -> PlayResult:
        available_trains = [train for train in table.trains.values() if train.is_public() or train == table.trains[self]]

        if self._play_on_first_train(table, available_trains):
            return self._can_play(table)
        else:
            self.log(table, "DRAW", f"cannot play, drawing...")
            if self.draw(table) == []: #no dominoes to draw
                self.log(table, "PASS", f"nothing to draw :(")
                return self._cannot_play(table)
            if self._play_on_first_train(table, available_trains):
                return self._can_play(table)
            else:
                self.log(table, "PASS", f"still cannot play")
                return self._cannot_play(table)
                
            
        



