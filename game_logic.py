from pieces import DominoPiece
from player import player

class Game:

    TARGET_SCORE = 100

    def __init__(self, player1_name, player2_name):
        self.player1 = player(player1_name)
        self.player2 = player(player2_name)
        self.current_player = self.player1
        self.board = []
        self.pieces = [DominoPiece(i, j) for i in range(7) for j in range(i, 7)]
        self.shuffle_pieces()

    def _deal(self):
        """Rebuild the full deck, clear both hands, deal 7 each.
        Returns the highest double dealt, or None if nobody got one."""
        self.pieces = [DominoPiece(i, j) for i in range(7) for j in range(i, 7)]
        self.shuffle_pieces()
        self.player1.reset_hand()
        self.player2.reset_hand()

        highest_double = None
        for _ in range(7):
            for p in (self.player1, self.player2):
                piece = self.draw_piece()
                p.add_piece(piece)
                if piece.is_double() and (highest_double is None or piece > highest_double):
                    highest_double = piece
        return highest_double

    def start_round(self):
        """Start one round: deal until somebody holds a double, then open with it."""
        self.board = []

        highest_double = None
        while highest_double is None:
            highest_double = self._deal()

        if highest_double in self.player1.get_hand():
            self.current_player = self.player1
        else:
            self.current_player = self.player2

        print(f"{self.current_player.name} has the highest double {highest_double} and opens.")
        self.play_piece(highest_double, "left")
        self.switch_turn()

    def start_game(self):
        """Start a whole match: zero the scores, then play the first round."""
        self.player1.reset_score()
        self.player2.reset_score()
        self.start_round()

    def update_scores(self):
        """Score the finished round. The winner takes the loser's pips.
        Returns the winning player, or None on a tie."""
        p1_pips = self.player1.sum_of_hand()
        p2_pips = self.player2.sum_of_hand()

        if not self.player1.get_hand():
            self.player1.update_score(p2_pips)
            return self.player1
        if not self.player2.get_hand():
            self.player2.update_score(p1_pips)
            return self.player2

        if p1_pips < p2_pips:
            self.player1.update_score(p2_pips - p1_pips)
            return self.player1
        if p2_pips < p1_pips:
            self.player2.update_score(p1_pips - p2_pips)
            return self.player2
        return None

    def shuffle_pieces(self):
        import random
        random.shuffle(self.pieces)

    def draw_piece(self):
        if self.pieces:
            return self.pieces.pop()
        else:
            raise ValueError("No more pieces to draw.")

    def switch_turn(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def get_legal_moves(self, player=None):
        """Every legal (piece, end) pair for this player. The engine reports
        the options; the caller - human or agent - picks one."""
        if player is None:
            player = self.current_player

        if not self.board:
            return [(piece, "left") for piece in player.get_hand()]

        left_end = self.board[0].num_1
        right_end = self.board[-1].num_2

        moves = []
        for piece in player.get_hand():
            if left_end in piece.get_nums():
                moves.append((piece, "left"))
            if right_end in piece.get_nums():
                moves.append((piece, "right"))
        return moves

    def play_piece(self, piece, end):
        if piece not in self.current_player.get_hand():
            raise ValueError(f"{piece} is not in {self.current_player.name}'s hand.")
        if not self.is_valid_move(piece, end):
            raise ValueError(f"{piece} cannot be played on the {end} end.")

        piece = DominoPiece(*piece.get_nums())   # copy, so we never flip the hand's object

        if not self.board:
            self.board.append(piece)
        elif end == "left":
            if piece.num_2 != self.board[0].num_1:
                piece.flip()
            self.board.insert(0, piece)
        elif end == "right":
            if piece.num_1 != self.board[-1].num_2:
                piece.flip()
            self.board.append(piece)
        else:
            raise ValueError("End must be 'left' or 'right'.")

        self.current_player.remove_piece(piece)

    def get_board(self):
        return [str(piece) for piece in self.board]

    def get_current_player(self):
        return self.current_player.name

    def is_valid_move(self, piece, end):
        if not self.board:
            return True

        if end == "left":
            return self.board[0].num_1 in piece.get_nums()
        if end == "right":
            return self.board[-1].num_2 in piece.get_nums()
        raise ValueError("End must be 'left' or 'right'.")

    def has_valid_move(self, player=None):
        return len(self.get_legal_moves(player)) > 0

    def draw_piece_for_player(self, player):
        """Draw one piece. Returns True if a piece was drawn, False if the
        boneyard is empty - so the caller's draw loop can actually stop."""
        if not self.pieces:
            return False
        drawn_piece = self.draw_piece()
        player.add_piece(drawn_piece)
        print(f"{player.name} drew {drawn_piece}.")
        return True

    def is_round_over(self):
        """True when somebody has gone out, or the round is blocked.
        Asks a question, prints nothing."""
        if not self.board:
            return False

        if not self.player1.get_hand() or not self.player2.get_hand():
            return True

        if (not self.pieces
                and not self.has_valid_move(self.player1)
                and not self.has_valid_move(self.player2)):
            return True

        return False

    def is_game_over(self):
        """True once either player reaches the target. Prints nothing."""
        return (self.player1.score >= self.TARGET_SCORE
                or self.player2.score >= self.TARGET_SCORE)

    def match_winner(self):
        if self.player1.score >= self.TARGET_SCORE:
            return self.player1
        if self.player2.score >= self.TARGET_SCORE:
            return self.player2
        return None
