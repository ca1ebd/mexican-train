from dataclasses import dataclass

from Player import Player
from PlayerAction import PlayerAction
from Enum import PlayResult
from Domino import Domino
from Train import Train

class LargestDominoFirstAvailableTrainPlayer(Player):

    def play(self, table, available_trains) -> PlayerAction:
        hand_table = self.hash_hand(table)
        # compile a list of the longest 
        for train in available_trains:
            if len(hand_table[train.tip]) > 0:
                domino = self.max_score(hand_table[train.tip])
                return PlayerAction(PlayResult.PLAY, domino, train)
        return PlayerAction(PlayResult.NOPLAY)
    
    def max_score(self, dominoes: list[Domino]) -> Domino:
        max = dominoes[0].score()
        max_domino = dominoes[0]
        for domino in dominoes:
            if domino.score() > max:
                max = domino.score()
                max_domino = domino
        return max_domino

@dataclass
class PotentialPlay:
    domino: Domino = None
    train: Train = None

class LargestDominoPlayer(Player):

    def play(self, table, available_trains) -> PlayerAction:
        hand_table = self.hash_hand(table)
        # compile a list of the longest
        potential_plays = []
        for train in available_trains:
            # if there are dominoes player can play on the train, add them to a list
            if len(hand_table[train.tip]) > 0:
                # domino = self.max_score(hand_table[train.tip])
                potential_plays += [PotentialPlay(domino, train) for domino in hand_table[train.tip]]
        if len(potential_plays) == 0:
            return PlayerAction(PlayResult.NOPLAY)
        max_play = self.max_score(potential_plays)
        return PlayerAction(PlayResult.PLAY, max_play.domino, max_play.train)
    
    def max_score(self, plays: list[PotentialPlay]) -> PotentialPlay:
        max = plays[0].domino.score()
        max_play = plays[0]
        for play in plays:
            if play.domino.score() > max:
                max = play.domino.score()
                max_play = play
        return max_play
