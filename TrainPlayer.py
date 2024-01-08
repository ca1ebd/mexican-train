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
    
class TrainBuilderPlayer(Player):
    def _hash_hand(self, hand):
        # hand_table = {x: [] for x in range(0, table.domino_double + 1)}
        hand_table = {}
        for domino in hand:
            if domino.left not in hand_table:
                hand_table[domino.left] = []
            hand_table[domino.left].append(domino)

            if domino.right not in hand_table:
                hand_table[domino.right] = []
            hand_table[domino.right].append(domino)
        return hand_table

    def play(self, table, available_trains) -> PlayerAction:
        potential_trains = []
        
        #map to associate potential trains with associated trains in case they are chosen
        train_map = {}
        for available_train in available_trains:
            potential_trains_for_available_train = self.get_all_potential_trains(available_train.tip, self.hand)
            potential_trains += potential_trains_for_available_train
            for potential_train in potential_trains_for_available_train:
                train_map[tuple(potential_train)] = available_train

        if len(potential_trains) == 0:
            return PlayerAction(PlayResult.NOPLAY)
        
        longest_trains = self.get_longest_trains(potential_trains)
        largest_longest_train = self.get_highest_value_train(longest_trains)
        return PlayerAction(PlayResult.PLAY, largest_longest_train[0], train_map[tuple(largest_longest_train)])
        # trains = self.get_all_potential_trains(available_trains[0].tip, self.hand)
        # pass

    def get_longest_trains(self, trains: list[list[Domino]]):
        if not trains:
            return []
        max_length = len(trains[0])
        for train in trains:
            if len(train) > max_length:
                max_length = len(train)
        return [train for train in trains if len(train) == max_length]
    
    #TODO maybe this should return a list... so that in the future the filter functions can be applied in different orders?
    def get_highest_value_train(self, trains: list[list[Domino]]):
        max_score = self.sum_train(trains[0])
        max_train = trains[0]
        for train in trains:
            score = self.sum_train(train)
            if score > max_score:
                max_score = score
                max_train = train
        return max_train

    def sum_train(self, trains: list[Domino]):
        return sum([domino.left + domino.right for domino in trains])


    def get_all_potential_trains(self, tip, hand) -> list[list[Domino]]:
        hand_table = self._hash_hand(hand)
        if tip not in hand_table:
            return []
        child_trains = []
        for domino in hand_table[tip]:
            new_hand = hand.copy()
            new_hand.remove(domino)
            child_trains += [[domino] + train for train in self.get_all_potential_trains(domino.other(tip), new_hand)]
        return child_trains if child_trains else [[domino]]

class BiasedTrainBuilderPlayer(TrainBuilderPlayer):
    def play(self, table, available_trains) -> PlayerAction:
        my_train = table.trains[self]
        other_trains = [train for train in available_trains if train != my_train]
        my_potential_trains = self.get_all_potential_trains(my_train.tip, self.hand)
        have_train = False
            

        if len(my_potential_trains) == 0:
            pass
            # play junk or draw
            # return PlayerAction(PlayResult.NOPLAY)
        
        longest_potential_trains = self.get_longest_trains(my_potential_trains)
        if longest_potential_trains:
            largest_longest_potential_train = self.get_highest_value_train(longest_potential_trains)
            have_train = True

        playable_junk = []
        if have_train:
            junk = [domino for domino in self.hand if domino not in largest_longest_potential_train]
            # playable_junk = []
            
            for train in other_trains:
                for domino in junk:
                    if train.tip == domino.left or train.tip == domino.right:
                        playable_junk.append(PotentialPlay(domino, train))

        # [PotentialPlay(domino, train) for domino in junk if domino.left == train.tip or domino.right == train.tip for train in other_trains]

        if playable_junk:
            return PlayerAction(PlayResult.PLAY, playable_junk[0].domino, playable_junk[0].train)

        if my_train in available_trains and have_train:
            return PlayerAction(PlayResult.PLAY, largest_longest_potential_train[0], my_train)
        
        hand_table = {train.tip: [] for train in available_trains}
        hand_table.update(self._hash_hand(self.hand))
        for train in available_trains:
            if hand_table[train.tip]:
                return PlayerAction(PlayResult.PLAY, hand_table[train.tip][0], train)
            
        return PlayerAction(PlayResult.NOPLAY)
        # trains = self.get_all_potential_trains(available_trains[0].tip, self.hand)
        # pass


