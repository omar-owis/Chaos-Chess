from ..helpers import *

from .piece import *


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.capture_directions = [LEFT, RIGHT, UP, DOWN, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
        self.extend_direction = True
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__),"graphics/white-queen.png"))\
            if color is WHITE else pygame.image.load(os.path.join(os.path.dirname(__file__),"graphics/black-queen.png"))

    def conditional_directions(self, **conditions):
        return []
