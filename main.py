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
from Player import LegalPlayer
from TrainPlayer import LargestDominoPlayer
from Stats import Stats

if __name__ == "__main__":
    players = (
        LargestDominoPlayer("Caleb", color="cyan"),
        LegalPlayer("Cailyn", color="pink"),
        LegalPlayer("GrandmaDot", color="red"),
        LegalPlayer("Pop", color="yellow")
    )

    game = Game(
        num_rounds=9, 
        players = players, 
        print_log=True, 
        # visual_round=True, 
        # visual_turn=True
    )
    result_table = game.start()
