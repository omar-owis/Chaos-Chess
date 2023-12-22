from ..helpers import *

from .piece import *


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.moved = False
        self.capture_directions = [LEFT, RIGHT, UP, DOWN]
        self.extend_direction = True
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__),"graphics/white-rook.png"))\
            if color is WHITE else pygame.image.load(os.path.join(os.path.dirname(__file__),"graphics/black-rook.png"))

    def conditional_directions(self, **conditions):
        pass
