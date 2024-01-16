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

    def player_has_spinner(self, table):
        hand_table = self.hash_hand()
        for domino in self.get_dominoes_for_number(table.round):
            if domino == table.spinner:
                domino_index = self.hand.index(domino)
                self.hand.pop(domino_index)
                
                return True
        return False
    
    def get_dominoes_for_number(self, number: int) -> list[Domino]:
        hand_table = self.hash_hand()
        if number not in hand_table:
            return []
        return hand_table[number]

    def hash_hand(self):
        # hand_table = {x: [] for x in range(0, table.domino_double + 1)}
        hand_table = {}
        for domino in self.hand:
            for side in [domino.left, domino.right]:
                if side not in hand_table:
                    hand_table[side] = []
                hand_table[side].append(domino)

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
        hand_table = self.hash_hand()
        for train in available_trains:
            if len(self.get_dominoes_for_number(train.tip)) > 0:
                domino = hand_table[train.tip][0]
                return PlayerAction(PlayResult.PLAY, domino, train)
        return PlayerAction(PlayResult.NOPLAY)
    
    
                
            
        



