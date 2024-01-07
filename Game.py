import random

from Visualizer import Visualizer
from Player import Player
from Domino import Domino, OldLady
from Table import Table
from Enum import PlayResult



class Game():
    def __init__(self, num_rounds: int, players: list[Player], print_log=False, visual_round=False, visual_turn=False):
        self.num_rounds = num_rounds
        self.players = players
        self.players_draw_num = 10
        self.spinner_draw_start_player_index = 0
        self.announcer = Player("Town Crier")
        self.print_log = print_log
        self.history = []
        self.visual_round = visual_round
        self.visual_turn = visual_turn

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
        self.log(table, self.announcer, group="FINAL", message="The game is over!")
        for key in table.player_scores.keys():
            self.log(table, self.announcer, group="FINAL", message=f"{key}: {table.player_scores[key]}")

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
            self.draw_hand_for_player(table, player)
            if player.player_has_spinner(table):
                start_player_index = player_index
                self.log(table, player, "SPINNER", "I have the spinner!")

        # draw to find the spinner if no one drew it when drawing hands
        if start_player_index is None:
            start_player_index = self.draw_start(table)
        
        current_player_index = start_player_index
        while not round_is_over:
            current_player = self.players[current_player_index]
            player_train = table.trains[current_player]
            # if uncovered trains has trains, pop the first one... or last?
            if len(table.uncovered_double_trains) > 0: # there is a double which needs to be covered
                available_trains = [table.uncovered_double_trains[0]]
            else:
                available_trains = [train for train in table.trains.values() if train.is_public() or train == player_train]
            play_result = self.play_player_recursive(table, current_player, available_trains, 1)
            if play_result == PlayResult.NOPLAY:
                pass_count += 1
                player_train.set_public(True)
                if pass_count > len(self.players):
                    if len(table.uncovered_double_trains) > 0:
                        table.uncovered_double_trains.pop()
                        pass_count = 0
                    else:
                        round_is_over = pass_count > len(self.players) and len(table.pool) == 0
                if round_is_over:
                    self.log(table, self.announcer, group="PASS", message="No one can play! The round is over and hands will be scored as-is")
            elif play_result == PlayResult.PLAY:
                pass_count = 0
                if len(current_player.hand) == 0:
                    self.log(table, current_player, "OUT", "went out!")
                    round_is_over = True

            if self.visual_turn:
                vis = Visualizer(table)
                vis.render()

            current_player_index = self._get_next_player_from_index(current_player_index)
        
        #round is over
        for player in self.players:
            score = player.score()
            table.player_scores[player] += score
            self.log(table, player, "ROUND SCORE", f"scored {score} this round, bringing their total to: {table.player_scores[player]}")

        if self.visual_round:
            vis = Visualizer(table)
            vis.render()

        self.visual_round = False

    # TODO this sucks, maybe replace with hashtable?
    def _game_has_domino_with_number(self, table: Table, number: int):
        for domino in table.pool:
            if domino.left == number or domino.right == number:
                return True
        for player in self.players:
            for domino in player.hand:
                if domino.left == number or domino.right == number:
                    return True
        return False
    
    def play_domino(self, table, player, train, domino):
        player.remove_domino_from_hand(domino)
        train.add_domino(domino)
        self.log(table, player, "PLACED", f"played {domino} on {train}")
        if train == table.trains[player] and train.is_public():
            train.set_public(False)
            self.log(table, player, "PLACED", f"penny removed!")

    def play_player_recursive(self, table, player, available_trains, draws):
        player_action = player.play(table, available_trains)
        if player_action.action == PlayResult.PLAY:
            self.play_domino(table, player, player_action.train, player_action.domino)
            if player_action.train in table.uncovered_double_trains:
                table.uncovered_double_trains.remove(player_action.train)
            if player_action.domino.is_double():
                # self.visual_round = True
                # add the train to uncovered trains if the pool or player hands have dominos to cover
                if self._game_has_domino_with_number(table, player_action.domino.left):
                    table.uncovered_double_trains.append(player_action.train)
                return self.play_player_recursive(table, player, available_trains, draws=1)
            else:
                return PlayResult.PLAY
        elif player_action.action == PlayResult.NOPLAY:
            if draws > 0:
                self.draw_for_player(table, player, 1)
                return self.play_player_recursive(table, player, available_trains, draws-1)
            else:
                return PlayResult.NOPLAY

    def check_uncovered_doubles(self, table: Table):
        uncovered_double_trains = []
        for player in table.trains: 
            if table.trains[player].dominoes[-1].is_double():
                uncovered_double_trains.append(table.trains[player])
            
    def draw_for_player(self, table, player, count=1):
        if len(table.pool) == 0:
            return []
        drawn = [table.pool.pop(random.randint(0, len(table.pool) - 1)) for x in range(0, count)]
        player.hand += drawn
        self.log(table, player, "DRAW", f"drew: {drawn}")
        return drawn
    
    def draw_hand_for_player(self, table, player):
        player.hand = []
        self.draw_for_player(table, player, count=self.players_draw_num)

    def draw_start(self, table: Table) -> int:
        start_player_index = None
        draw_player_index = self._get_spinner_draw_start_player()
        while start_player_index is None:
            current_player = self.players[draw_player_index]
            self.draw_for_player(table, current_player)
            if current_player.player_has_spinner(table):
                start_player_index = draw_player_index
            else:
                draw_player_index = self._get_next_player_from_index(draw_player_index)
        assert start_player_index is not None
        return start_player_index
    
    def log(self, table, player, group, message):
        filled = f"[{table.round}][{player}][{group}]: {message}"
        self.history.append(filled)
        if self.print_log:
            print(filled)

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

