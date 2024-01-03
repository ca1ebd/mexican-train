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
    num_games = 1

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
    
    # print("\n".join(result.history))
    print(tallies)
    pass