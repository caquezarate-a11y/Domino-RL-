from pieces import DominoPiece
from player import player
from game_logic import Game


def ask_for_move(game):
    """Show the legal moves and let the human pick one. All input() lives here."""
    moves = game.get_legal_moves()
    print("Legal moves:")
    for i, (piece, end) in enumerate(moves):
        print(f"  {i}: play {piece} on the {end} end")

    while True:
        choice = input("Pick a move number: ")
        try:
            return moves[int(choice)]
        except (ValueError, IndexError):
            print("That is not one of the numbers above.")


if __name__ == "__main__":
    player1_name = input("Enter name for Player 1: ")
    player2_name = input("Enter name for Player 2: ")
    game = Game(player1_name, player2_name)

    game.start_game()

    while not game.is_game_over():

        while not game.is_round_over():
            print(f"\nBoard: {' '.join(game.get_board())}")
            current = game.current_player
            print(f"{current.name}'s turn. Hand: {[str(p) for p in current.get_hand()]}")

            # draw until playable, or until the boneyard runs out
            while not game.has_valid_move() and game.draw_piece_for_player(current):
                pass

            if not game.has_valid_move():
                print(f"{current.name} is blocked and cannot draw. Passing.")
                game.switch_turn()
                continue

            piece, end = ask_for_move(game)
            game.play_piece(piece, end)
            game.switch_turn()

        # --- round over ---
        print(f"\nFinal board: {' '.join(game.get_board())}")
        print(f"{game.player1.name} holds {[str(p) for p in game.player1.get_hand()]}")
        print(f"{game.player2.name} holds {[str(p) for p in game.player2.get_hand()]}")

        winner = game.update_scores()
        print(f"Round winner: {winner.name}" if winner else "Round is a tie.")
        print(f"Score: {game.player1.name} {game.player1.score} - "
              f"{game.player2.name} {game.player2.score}")

        if not game.is_game_over():
            input("\nPress Enter for the next round...")
            game.start_round()

    print(f"\n{game.match_winner().name} wins the match!")
