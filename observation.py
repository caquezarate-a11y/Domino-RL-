import numpy as np
from actions import PIECE_INDEX          


def full_observation(game, me):
    """The 72 numbers `me` is allowed to see. Same length every turn."""
    opponent = game.player2 if me is game.player1 else game.player1

    my_tiles = np.zeros(28, dtype=np.float32)
    for p in me.get_hand():
        my_tiles[PIECE_INDEX[frozenset(p.get_nums())]] = 1

    played = np.zeros(28, dtype=np.float32)
    for p in game.board:
        played[PIECE_INDEX[frozenset(p.get_nums())]] = 1

    left_end  = np.zeros(7, dtype=np.float32)
    right_end = np.zeros(7, dtype=np.float32)
    if game.board:                                  # board is empty before the first move
        left_end[game.board[0].num_1]   = 1
        right_end[game.board[-1].num_2] = 1

    counts = np.array([len(opponent.get_hand()), len(game.pieces)], dtype=np.float32)

    return np.concatenate([my_tiles, played, left_end, right_end, counts])

