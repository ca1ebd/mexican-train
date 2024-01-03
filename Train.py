from Domino import Domino

class Train():
    def __init__(self, name: str, tip: int, public=False):
        self.name = name
        self.dominoes = []
        self.public = public
        self.tip = tip

    def set_public(self, is_public: bool):
        self.public = is_public
    
    def is_public(self):
        return self.public
    
    def add_domino(self, domino: Domino):
        if domino.right == self.tip:
            domino.swap()

        if domino.left == self.tip:
            self.tip = domino.right
            self.dominoes.append(domino)
        else:
            print(f"Error, domino {domino} cannot be added to train with tip {self.tip}")

    def reset(self, round):
        self.tip = round
        self.dominoes.clear()

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    
    def __repr__(self) -> str:
        return f"{self.name}: {self.dominoes}"
    
class CommonTrain(Train):
    def __init__(self, tip: int):
        super().__init__("CommonTrain", tip, public=True)

    # consider pulling out a PlayerTrain subclass and defining there, rather than override here
    def set_public(self, is_public: bool):
        pass

    