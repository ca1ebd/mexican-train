from Enum import PlayResult
from dataclasses import dataclass
from Domino import Domino
from Train import Train

@dataclass
class PlayerAction:
    action: PlayResult
    domino: Domino = None
    train: Train = None

    def __repr__(self) -> str:
        if self.action == PlayResult.PLAY:
            return f"{self.action}: {self.domino} -> {self.train}"
        else:
            return f"{self.action}"
    