from Domino import Domino
from Player import Player
from Train import Train, CommonTrain

class Table:
    def __init__(self, pool: list[Domino], players: list[Player], round=9) -> None:
        self.pool = pool
        self.trains = {player: Train(player.name + "Train", tip=round) for player in players} 
        self.trains[Player("Common", is_real=False, color="orange")] = CommonTrain(tip=round)
        self.spinner = Domino(round, round)
        self.round = round
        self.played_spinner = False
        self.uncovered_double_trains = []