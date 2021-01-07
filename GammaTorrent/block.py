__author__ = ["Manav Vagrecha", "Shreyansh Shah", "Devam Shah"]
__email__ = ["manavkumar.v@ahduni.edu.in", "shreyansh.s1@ahduni.edu.in", "devam.s1@ahduni.edu.in"]

from enum import Enum

BLOCK_SIZE = 2 ** 14

class State(Enum):
        EMPTY = 0
        PARTIAL = 1
        FULL = 2

class Block():
    def __init__(self, state: State=State.EMPTY, block_size: int = BLOCK_SIZE, data: bytes = b'', last_seen: float = 0):
        self.state= state
        self.block_size= block_size
        self.data= data
        self.last_seen= last_seen

    def __str__(self):
        return "%s - %d - %d - %d" % (self.state, self.block_size, len(self.data), self.last_seen)