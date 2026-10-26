"""Fixed action numbering for the RL agent.

There are 28 dominoes and 2 ends, so 56 possible actions. Action number i
always means the same (tile, end) pair, forever - that is what lets a network
have a fixed-size output layer.

Do NOT "tidy" ALL_PIECES into a set or reorder it. The numbering must stay
stable across runs, or a saved Q-table/network silently means something else.

This is the piece that belongs in domino_env.py when you build it.
"""
import numpy as np
from pieces import DominoPiece

ALL_PIECES  = [(i, j) for i in range(7) for j in range(i, 7)]      # 28, order fixed forever
PIECE_INDEX = {frozenset(p): k for k, p in enumerate(ALL_PIECES)}  # frozenset: [3|5] == [5|3]
N_ACTIONS   = len(ALL_PIECES) * 2                                  # 56


def encode_action(piece, end):
    """(DominoPiece, 'left'|'right') -> action number 0..55"""
    return PIECE_INDEX[frozenset(piece.get_nums())] * 2 + (0 if end == "left" else 1)


def decode_action(a):
    """action number 0..55 -> (DominoPiece, 'left'|'right')"""
    nums = ALL_PIECES[a // 2]
    return DominoPiece(*nums), ("left" if a % 2 == 0 else "right")


def legal_mask(game):
    """Boolean array of length 56: which actions are legal right now."""
    mask = np.zeros(N_ACTIONS, dtype=bool)
    for piece, end in game.get_legal_moves():
        mask[encode_action(piece, end)] = True
    return mask


if __name__ == "__main__":
    import random, io, contextlib
    from game_logic import Game

    print(f"N_ACTIONS = {N_ACTIONS}")
    print(f"unique piece keys: {len(PIECE_INDEX)} (need 28, no collisions)")

    bad = 0
    for a in range(N_ACTIONS):
        piece, end = decode_action(a)
        if encode_action(piece, end) != a:
            bad += 1
        piece.flip()                      # same tile, other way round
        if encode_action(piece, end) != a:
            bad += 1
    print(f"round-trip: {N_ACTIONS * 2} checks, {bad} failures")

    random.seed(7)
    g = Game("A", "B")
    with contextlib.redirect_stdout(io.StringIO()):
        g.start_game()
    mask = legal_mask(g)
    print(f"board {' '.join(g.get_board())}")
    print(f"hand  {[str(p) for p in g.current_player.get_hand()]}")
    print(f"legal action numbers: {np.flatnonzero(mask).tolist()}")
