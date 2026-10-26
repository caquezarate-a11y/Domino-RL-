from pieces import DominoPiece

class player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = []

    def update_score(self, points):
        self.score += points

    def reset_score(self):
        self.score = 0

    def reset_hand(self):
        self.hand = []

    def add_piece(self, piece):
        self.hand.append(piece)

    def get_hand(self):
        return self.hand

    def remove_piece(self, piece):
        if piece in self.hand:
            self.hand.remove(piece)
        else:
            raise ValueError("Piece not found in hand.")

    def sum_of_hand(self):
        return sum(piece.sum() for piece in self.hand)
