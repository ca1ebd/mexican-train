'''
A program to simulate dominoes game called Mexican Train
Copyright (C) 2024 Caleb Dudley

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from Game import Game
from Player import Player, LegalPlayer

if __name__ == "__main__":
    players = (
        LegalPlayer("Caleb"),
        LegalPlayer("Cailyn"),
        LegalPlayer("GrandmaDot"),
        LegalPlayer("Pop")
    )

    tallies = {player: 0 for player in players}
    num_games = 10

    for i in range(0, num_games):
        game = Game(num_rounds=9, players = players, print_log=True)
        result_table = game.start()

        final_scores = result_table.player_scores
        min = final_scores[players[0]]
        winner = players[0]
        for player in players:
            if final_scores[player] < min:
                winner = player
                min = final_scores[winner]

        tallies[winner] += 1

    print(tallies)