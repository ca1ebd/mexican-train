from Player import Player

class Stats:
    def __init__(self, players: list[Player]):
        self.counters = {}
        self.players = players

    def increment_counter(self, counter: str, player: Player):
        if counter not in self.counters:
            self.counters[counter] = {player: 0 for player in self.players}
        self.counters[counter][player] += 1

    def print_counters(self):
        for counter_name in self.counters:
            print(f"{counter_name}:")
            for player, counter in self.counters[counter_name].items():
                print(f"\t{player}: {counter}")

