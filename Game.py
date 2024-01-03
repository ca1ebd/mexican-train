import random

from Player import Player
from Domino import Domino, OldLady
from Table import Table
from Enum import PlayResult


class Game():
    def __init__(self, num_rounds: int, players: list[Player], print_log=False):
        self.num_rounds = num_rounds
        self.players = players
        self.players_draw_num = 10
        self.spinner_draw_start_player_index = 0
        self.announcer = Player("Town Crier")
        self.print_log = print_log
        

    def start(self):
        table = Table(self._generate_dominoes(self.num_rounds), self.players, print_log=self.print_log)
        self.play_game(table, self.num_rounds)
        self.game_over(table)
        return table

    def play_game(self, table: Table, round: int):
        table.pool = self._shuffle_pool(table.original_pool)
        table.set_round(round)
        self.play_round(table)

        if(round == 0):
            return
        else:
            self.play_game(table, round - 1)

    def game_over(self, table: Table):
        table.log(self.announcer, group="FINAL", message="The game is over!")
        for key in table.player_scores.keys():
            table.log(self.announcer, group="FINAL", message=f"{key}: {table.player_scores[key]}")

    def _get_next_player_from_index(self, index):
        next_player = (index + 1) % len(self.players)
        return next_player

    def _get_spinner_draw_start_player(self):
        player_index = self.spinner_draw_start_player_index

        # increment the player to start the draw next time
        self.spinner_draw_start_player_index = self._get_next_player_from_index(player_index)

        return player_index

    def play_round(self, table: Table):
        round_is_over = False
        start_player_index = None
        pass_count = 0
        for player_index in range(0, len(self.players)):
            player = self.players[player_index]
            player.draw_hand(table, self.players_draw_num)
            if player.player_has_spinner(table):
                start_player_index = player_index

        # draw to find the spinner if no one drew it when drawing hands
        if start_player_index is None:
            start_player_index = self.draw_start(table)
        
        current_player_index = start_player_index
        while not round_is_over:
            current_player = self.players[current_player_index]
            play_result = current_player.play(table)
            if play_result == PlayResult.OUT:
                round_is_over = True
                # end round
            elif play_result == PlayResult.PASS:
                pass_count += 1
                round_is_over = pass_count > len(self.players) and len(table.pool) == 0
                if round_is_over:
                    table.log(self.announcer, group="PASS", message="No one can play! The round is over and hands will be scored as-is")
            elif play_result == PlayResult.NEXT:
                pass_count = 0
            
            current_player_index = self._get_next_player_from_index(current_player_index)
        
        #round is over
        for player in self.players:
            score = player.score()
            table.player_scores[player] += score
            table.log(player, "ROUND SCORE", f"scored {score} this round, bringing their total to: {table.player_scores[player]}")
            
        


    def draw_start(self, table: Table) -> int:
        start_player_index = None
        draw_player_index = self._get_spinner_draw_start_player()
        while start_player_index is None:
            current_player = self.players[draw_player_index]
            current_player.draw(table)
            if current_player.player_has_spinner(table):
                start_player_index = draw_player_index
            else:
                draw_player_index = self._get_next_player_from_index(draw_player_index)
        assert start_player_index is not None
        return start_player_index

    def _generate_dominoes(self, num_rounds):
        pool = []
        for i in range(0, num_rounds + 1):
            for j in range(i, num_rounds + 1):
                if i == j == 0:
                    pool.append(OldLady())
                else:
                    pool.append(Domino(i, j))
        return pool

    def _shuffle_pool(self, pool):
        shuffled_pool = []
        pool = pool.copy()
        while(len(pool) > 0):
            shuffled_pool.append(pool.pop(random.randint(0, len(pool) - 1)))
        return shuffled_pool

