class Domino:
    def __init__(self, left: int, right: int):
        self.left = left
        self.right = right

    def get_cost(self):
        return self.left + self.right
    
    def swap(self):
        swap = self.left
        self.left = self.right
        self.right = swap

    # returns the other number on the domino
    def other(self, number: int):
        if self.left == number:
            return self.right
        if self.right == number:
            return self.left

    def score(self):
        return self.left + self.right
    
    def is_double(self):
        return self.left == self.right

    def __eq__(self, __value: object) -> bool:
        return (
            self.left == __value.left and self.right == __value.right
            or
            self.left == __value.right and self.right == __value.left
        )
    
    def __repr__(self) -> str:
        return f"{self.left}|{self.right}"
    
    def __hash__(self):
        return hash(repr(self))
    
class OldLady(Domino):
    def __init__(self):
        super().__init__(0, 0)

    def score(self):
        return 50