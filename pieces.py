

class DominoPiece(object):

    def __init__ (self, num_1, num_2):

        if num_1 not in range(0, 7) or num_2 not in range(0, 7):
            raise ValueError("Domino numbers must be between 0 and 6.")

        
        self.num_1 = num_1
        self.num_2 = num_2

    def __str__(self):
        return f"[{self.num_1}|{self.num_2}]"

    def flip(self):
        self.num_1, self.num_2 = self.num_2, self.num_1

    def is_double(self):
        return self.num_1 == self.num_2

    def sum(self):
        return self.num_1 + self.num_2

    def get_nums(self):
        return (self.num_1, self.num_2)

    def __eq__(self, other):

        if not isinstance(other, DominoPiece):
            return NotImplemented

        if self.num_1 == other.num_1 and self.num_2 == other.num_2:
            return True
        elif self.num_1 == other.num_2 and self.num_2 == other.num_1:
            return True
        else:
            return False

    def __gt__(self, other):
        return self.sum() > other.sum()

    def __lt__(self, other):
        return self.sum() < other.sum()

    def __hash__(self):
        return hash(frozenset((self.num_1, self.num_2)))

    
    

    