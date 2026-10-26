from player import player
from pieces import DominoPiece
from random import shuffle
from game_logic import Game

class Board:
    def __init__(self, game):
        self.game = game


    def display_board(self):
        board_str = "Current Board: "
        if not self.game.board:
            board_str += "Empty"
        else:
            board_str += " ".join(str(piece) for piece in self.game.board)
        print(board_str)


    def display_player_hands(self):
        print(f"{self.game.player1.name}'s hand: {[str(piece) for piece in self.game.player1.get_hand()]}")
        print(f"{self.game.player2.name}'s hand: {[str(piece) for piece in self.game.player2.get_hand()]}")

    