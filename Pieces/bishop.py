from ..helpers import *

from .piece import *


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.capture_directions = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
        self.extend_direction = True
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__),"graphics/white-bishop.png"))\
            if color is WHITE else pygame.image.load(os.path.join(os.path.dirname(__file__),"graphics/black-bishop.png"))

    def conditional_directions(self, **conditions):
        return []
