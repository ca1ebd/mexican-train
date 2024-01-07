from Game import Game
from Player import LegalPlayer

if __name__ == "__main__":
    players = (
        LegalPlayer("Caleb", color="cyan"),
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
