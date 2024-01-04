from Domino import Domino
from Player import Player
from Train import Train, CommonTrain

class Table:
    def __init__(self, pool: list[Domino], players: list[Player], domino_double=9, print_log=False) -> None:
        self.original_pool = pool.copy() # move to game
        self.pool = pool
        self.trains = {player: Train(player.name + "Train", tip=domino_double) for player in players} 
        self.trains[Player("Common", is_real=False, color="orange")] = CommonTrain(tip=domino_double)
        self.player_scores = {player: 0 for player in players} # move to game
        self.domino_double = domino_double # move to game
        self.spinner = Domino(-1, -1)
        self.round = -1
        self.played_spinner = False
        self.history: list[str] = [] # move to game
        self.print_log = print_log # move to game

    def _reset_trains(self, round): # change to create only, no reset
        for player in self.trains.keys():
            self.trains[player].reset(round)

    def set_round(self, round_num): # move to game
        self.round = round_num
        self.spinner = Domino(round_num, round_num)
        self.played_spinner = False
        self._reset_trains(round_num)

    def log(self, player, group, message): # move to game
        pass
        # filled = f"[{self.round}][{player}][{group}]: {message}"
        # self.history.append(filled)
        # if self.print_log:
        #     print(filled)