"""Headless random-vs-random self-play. No input(), no human, no keyboard.
If the engine is sound this runs thousands of matches without hanging."""
import random, io, contextlib, collections
from game_logic import Game
from pieces import DominoPiece


def play_match(seed):
    random.seed(seed)
    game = Game("A", "B")
    game.start_game()

    turns = 0
    while not game.is_game_over():
        while not game.is_round_over():
            turns += 1
            if turns > 5000:
                raise RuntimeError("match did not terminate")

            while not game.has_valid_move() and game.draw_piece_for_player(game.current_player):
                pass
            if not game.has_valid_move():
                game.switch_turn()
                continue

            piece, end = random.choice(game.get_legal_moves())
            game.play_piece(piece, end)
            game.switch_turn()

        game.update_scores()
        if not game.is_game_over():
            game.start_round()

    # integrity check: all 28 tiles still accounted for
    total = len(game.player1.hand) + len(game.player2.hand) + len(game.pieces) + len(game.board)
    seen = [str(p) for p in game.board]
    if len(set(seen)) != len(seen):
        raise RuntimeError(f"duplicate tile on board: {seen}")
    if total != 28:
        raise RuntimeError(f"tile count is {total}, expected 28")

    # integrity check: the board is a legal chain
    for a, b in zip(game.board, game.board[1:]):
        if a.num_2 != b.num_1:
            raise RuntimeError(f"broken chain: {a} then {b}")

    return game.match_winner().name, turns


print("Running 2000 random self-play matches...")
wins = collections.Counter()
total_turns = 0
with contextlib.redirect_stdout(io.StringIO()):
    for seed in range(2000):
        w, t = play_match(seed)
        wins[w] += 1
        total_turns += t

print(f"  completed: {sum(wins.values())}/2000 matches, no hangs, no crashes")
print(f"  wins: {dict(wins)}")
print(f"  avg turns per match: {total_turns / 2000:.1f}")
print("  all matches: 28 tiles accounted for, board chain legal, no duplicate tiles")
